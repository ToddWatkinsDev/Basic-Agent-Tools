import os, sys, shlex

# Fix paths — must be before any local imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
sys.path.insert(0, project_root)

from toolsets import TOOLSETS
from openai import OpenAI
import subprocess, json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

with open("qwen/AGENT_CONTEXT.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

def build_tools():
    tools = []
    for category, paths in TOOLSETS.items():
        for path in paths:
            script_name = path.split("/")[-1].replace(".py", "")
            tools.append({
                "type": "function",
                "function": {
                    "name": script_name,
                    "description": f"Runs {script_name}. Part of {category}.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "args": {
                                "type": "string",
                                "description": "Space-separated command line arguments, Never leave empty if the tool needs a path or any argument. If no arguments are needed, pass an empty string."
                            }
                        },
                        "required": []
                    }
                }
            })
    return tools

def run_tool(tool_name: str, args: str = "") -> str:
    for category, paths in TOOLSETS.items():
        for path in paths:
            if path.split("/")[-1].replace(".py", "") == tool_name:
                # Use shlex.split so quoted paths with spaces are handled correctly
                cmd = ["python", path] + (shlex.split(args) if args else [])
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                return result.stdout or result.stderr
    return f"Unknown tool: {tool_name}"

def get_response(messages, force_answer: bool, show_thinking: bool):
    """Get a response, streaming thinking tokens if requested."""
    if show_thinking:
        # Streaming mode — print thinking in real time
        print("\n💭 Thinking:\n")
        stream = client.chat.completions.create(
            model="qwen3:4b",#qwen3:8b(Bigger Model), qwen3:4b(medium), qwen3:1.7b(small)
            messages=messages,
            tools=build_tools(),
            tool_choice="none" if force_answer else "auto",
            extra_body={"think": True},
            stream=True
        )

        # Collect streamed chunks
        reasoning_buf = ""
        content_buf = ""
        tool_calls_buf = {}
        in_thinking = False

        for chunk in stream:
            delta = chunk.choices[0].delta

            # Stream reasoning/thinking tokens
            if hasattr(delta, "reasoning") and delta.reasoning:
                if not in_thinking:
                    in_thinking = True
                print(delta.reasoning, end="", flush=True)
                reasoning_buf += delta.reasoning

            # Stream content tokens
            if delta.content:
                if in_thinking:
                    print("\n\n💬 Response:\n")
                    in_thinking = False
                print(delta.content, end="", flush=True)
                content_buf += delta.content

            # Collect tool calls
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in tool_calls_buf:
                        tool_calls_buf[idx] = {
                            "id": tc.id or "",
                            "name": "",
                            "arguments": ""
                        }
                    if tc.id:
                        tool_calls_buf[idx]["id"] = tc.id
                    if tc.function.name:
                        tool_calls_buf[idx]["name"] += tc.function.name
                    if tc.function.arguments:
                        tool_calls_buf[idx]["arguments"] += tc.function.arguments

        print()  # newline after streamed output

        # Reconstruct a message-like object
        class FakeMessage:
            def __init__(self, content, reasoning, tool_calls):
                self.content = content
                self.reasoning = reasoning
                self.tool_calls = tool_calls or None

        class FakeToolCall:
            def __init__(self, id, name, arguments):
                self.id = id
                self.function = type("F", (), {"name": name, "arguments": arguments})()

        fake_tool_calls = [
            FakeToolCall(v["id"], v["name"], v["arguments"])
            for v in tool_calls_buf.values()
        ] if tool_calls_buf else None

        return FakeMessage(content_buf, reasoning_buf, fake_tool_calls)

    else:
        # Normal non-streaming mode
        response = client.chat.completions.create(
            model="qwen3:4b",
            messages=messages,
            tools=build_tools(),
            tool_choice="none" if force_answer else "auto",
            extra_body={"think": False}
        )
        return response.choices[0].message

def chat(user_message: str, show_thinking: bool = False):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    print(f"\n📨 User: {user_message}")
    print("─" * 50)

    max_iterations = 15
    iteration = 0
    last_tool_call = None
    repeat_count = 0

    while iteration < max_iterations:
        iteration += 1
        if not show_thinking:
            print("🤔 Thinking...")

        force_answer = repeat_count >= 3
        msg = get_response(messages, force_answer, show_thinking)

        if not msg.tool_calls:
            answer = msg.content or msg.reasoning or "No response."
            if not show_thinking:
                print(f"\n✅ Final Answer:\n{answer}")
            else:
                print(f"\n✅ Done.")
            break

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                }
                for tc in msg.tool_calls
            ]
        })

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments).get("args", "")
            current_call = (tc.function.name, args)

            if current_call == last_tool_call:
                repeat_count += 1
            else:
                repeat_count = 0
            last_tool_call = current_call

            print(f"\n🔧 Tool call: {tc.function.name}({args})")
            output = run_tool(tc.function.name, args)
            print(f"📤 Result: {output}")
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": output
            })
        print("─" * 50)

    if iteration >= max_iterations:
        print("⚠️ Max iterations reached.")

if __name__ == "__main__":
    # Parse --think flag from args
    args = sys.argv[1:]
    show_thinking = "--think" in args
    if show_thinking:
        args.remove("--think")

    user_input = " ".join(args) or input("You: ")
    chat(user_input, show_thinking=show_thinking)
