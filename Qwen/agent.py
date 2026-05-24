import subprocess, json, sys
from openai import OpenAI
from toolsets import TOOLSETS  # your existing registry

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Load AGENT_CONTEXT.md as the system prompt
with open("AGENT_CONTEXT.md", "r") as f:
    system_prompt = f.read()

# Build tool definitions for Qwen3 from your TOOLSETS registry
def build_tools():
    tools = []
    for name, path in TOOLSETS.items():
        tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": f"Run {path}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "args": {
                            "type": "string",
                            "description": "Space-separated command line arguments"
                        }
                    },
                    "required": []
                }
            }
        })
    return tools

def run_tool(tool_name: str, args: str = "") -> str:
    path = TOOLSETS.get(tool_name)
    if not path:
        return f"Unknown tool: {tool_name}"
    cmd = ["python", path] + args.split() if args else ["python", path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout or result.stderr

def chat(user_message: str):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    while True:
        response = client.chat.completions.create(
            model="qwen3:4b",
            messages=messages,
            tools=build_tools(),
            tool_choice="auto"
        )
        msg = response.choices[0].message
        
        # If no tool call, we're done
        if not msg.tool_calls:
            print(f"\nAgent: {msg.content}")
            break
        
        # Execute each tool call
        messages.append(msg)
        for tc in msg.tool_calls:
            fn = tc.function
            args = json.loads(fn.arguments).get("args", "")
            print(f"  → Running: {fn.name} {args}")
            output = run_tool(fn.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": output
            })

if __name__ == "__main__":
    user_input = " ".join(sys.argv[1:]) or input("You: ")
    chat(user_input)