import os, sys, shlex, json, subprocess
from openai import OpenAI

# Fix paths — must be before any local imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
sys.path.insert(0, project_root)

from toolsets import TOOLSETS

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

with open("orchestrator/AGENT_PROMPT.md", "r", encoding="utf-8") as f:
    agent_context = f.read()

# ─────────────────────────────────────────────
# TOOL REGISTRY
# ─────────────────────────────────────────────
def _tool_entry(path: str, description: str) -> dict:
    """Build a single OpenAI tool definition from a (path, description) tuple."""
    script_name = path.split("/")[-1].replace(".py", "")
    return {
        "type": "function",
        "function": {
            "name": script_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    "args": {
                        "type": "string",
                        "description": "Command-line arguments exactly as described above. Must not be empty if the tool requires input."
                    }
                },
                "required": []
            }
        }
    }

def build_tools_for_category(category: str):
    return [
        _tool_entry(path, description)
        for path, description in TOOLSETS.get(category, [])
    ]

def build_all_tools():
    return [
        _tool_entry(path, description)
        for entries in TOOLSETS.values()
        for path, description in entries
    ]

def run_tool(tool_name: str, args: str = "") -> str:
    for entries in TOOLSETS.values():
        for path, _ in entries:
            if path.split("/")[-1].replace(".py", "") == tool_name:
                cmd = ["python", path] + (shlex.split(args) if args else [])
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                return result.stdout or result.stderr
    return f"Unknown tool: {tool_name}"

# ─────────────────────────────────────────────
# AGENT LOOP
# ─────────────────────────────────────────────
def chat(user_message: str, category: str = None, show_thinking: bool = False):
    """
    Run the agent on a user message.
    - category: restrict tools to a single toolset category (for worker mode)
    - category=None: give agent access to all tools (standalone mode)
    """
    tools = build_tools_for_category(category) if category else build_all_tools()

    # agent_context IS the full system prompt — no hardcoded prefix needed
    messages = [
        {"role": "system", "content": agent_context},
        {"role": "user", "content": user_message}
    ]

    print(f"\n\u{1F4E8} Task: {user_message}")
    if category:
        print(f"\u{1F5C2}  Category: {category}")
    print("\u2500" * 50)

    max_iterations = 15
    iteration = 0
    last_tool_call = None
    repeat_count = 0

    while iteration < max_iterations:
        iteration += 1

        # Force a tool call on iteration 1 — prevents think-and-quit
        if repeat_count >= 3:
            tool_choice = "none"       # model is looping, force a text answer
        elif iteration == 1:
            tool_choice = "required"   # must act, not just think
        else:
            tool_choice = "auto"

        if show_thinking:
            print("\n\U0001F4AD Thinking:\n")
            stream = client.chat.completions.create(
                model="qwen3:1.7b",
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                extra_body={"think": True},
                stream=True
            )

            reasoning_buf, content_buf, tool_calls_buf = "", "", {}
            in_thinking = False

            for chunk in stream:
                delta = chunk.choices[0].delta

                if hasattr(delta, "reasoning") and delta.reasoning:
                    if not in_thinking:
                        in_thinking = True
                    print(delta.reasoning, end="", flush=True)
                    reasoning_buf += delta.reasoning

                if delta.content:
                    if in_thinking:
                        print("\n\n\U0001F4AC Response:\n")
                        in_thinking = False
                    print(delta.content, end="", flush=True)
                    content_buf += delta.content

                if delta.tool_calls:
                    for tc in delta.tool_calls:
                        idx = tc.index
                        if idx not in tool_calls_buf:
                            tool_calls_buf[idx] = {"id": tc.id or "", "name": "", "arguments": ""}
                        if tc.id:
                            tool_calls_buf[idx]["id"] = tc.id
                        if tc.function.name:
                            tool_calls_buf[idx]["name"] += tc.function.name
                        if tc.function.arguments:
                            tool_calls_buf[idx]["arguments"] += tc.function.arguments

            print()

            class FakeMessage:
                def __init__(self, content, reasoning, tool_calls):
                    self.content = content
                    self.reasoning = reasoning
                    self.tool_calls = tool_calls or None

            class FakeToolCall:
                def __init__(self, id, name, arguments):
                    self.id = id
                    self.function = type("F", (), {"name": name, "arguments": arguments})()

            fake_tcs = [FakeToolCall(v["id"], v["name"], v["arguments"]) for v in tool_calls_buf.values()]
            msg = FakeMessage(content_buf, reasoning_buf, fake_tcs if fake_tcs else None)

        else:
            print("\U0001F914 Working...")
            response = client.chat.completions.create(
                model="qwen3:1.7b",
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                extra_body={"think": False}
            )
            msg = response.choices[0].message

        # ── No tool call → final answer ──
        if not msg.tool_calls:
            answer = msg.content or getattr(msg, "reasoning", None) or "No response."
            print(f"\n\u2705 Done:\n{answer}")
            return answer

        # ── Append assistant turn ──
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

        # ── Execute each tool call ──
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments).get("args", "")
            current_call = (tc.function.name, args)

            repeat_count = repeat_count + 1 if current_call == last_tool_call else 0
            last_tool_call = current_call

            print(f"\n\U0001F527 {tc.function.name}({args})")
            output = run_tool(tc.function.name, args)
            print(f"\U0001F4E4 {output}")

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": output
            })

        print("\u2500" * 50)

    print("\u26A0\uFE0F Max iterations reached.")
    return "Max iterations reached."

# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    show_thinking = "--think" in args
    if show_thinking:
        args.remove("--think")

    # Optional: --category <name> restricts tools to one toolset
    category = None
    if "--category" in args:
        idx = args.index("--category")
        category = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    user_input = " ".join(args) or input("You: ")
    chat(user_input, category=category, show_thinking=show_thinking)
