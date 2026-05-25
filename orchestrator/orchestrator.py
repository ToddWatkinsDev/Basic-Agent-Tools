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

with open("orchestrator/ORCHESTRATOR_PROMPT.md", "r", encoding="utf-8") as f:
    ORCHESTRATOR_PROMPT = f.read()

# Map the short worker names used in ORCHESTRATOR_PROMPT to TOOLSETS keys.
WORKER_CATEGORY_MAP = {
    "archive":   "archive_utilities",
    "data":      "data_utilities",
    "file":      "file_utilities",
    "graphing":  "graphing_utilities",
    "math":      "math_utilities",
    "ml":        "ml_utilities",
    "network":   "network_utilities",
    "reporting": "reporting_utilities",
    "system":    "system_utilities",
    "web":       "web_utilities",
}

def resolve_category(name: str) -> str:
    return WORKER_CATEGORY_MAP.get(name, name)

def _args_hint(description: str) -> str:
    """Extract the Args/Example line from a tool description for use as the args field hint."""
    for line in description.split("."):
        if "Args:" in line or "Example:" in line:
            return line.strip()
    return "Provide the required arguments as a space-separated string. Never leave empty if the tool needs input."

def extract_args(arguments_json: str) -> str:
    """Robustly extract the args string from the model's tool call JSON.

    Small models (qwen3:1.7b) sometimes ignore the schema and invent parameter
    names like num1/num2, a/b, n1, numbers, query, etc. instead of using 'args'.
    This function normalises ALL of those cases into a single args string so the
    tool script receives its expected command-line arguments regardless of what
    the model decided to call the parameters.
    """
    try:
        params = json.loads(arguments_json)
    except (json.JSONDecodeError, TypeError):
        return ""

    if "args" in params:
        return str(params["args"]).strip()

    # Model invented its own parameter names — join all values in declaration order.
    SKIP_KEYS = {"type", "description", "required", "properties", "schema"}
    values = [
        str(v).strip()
        for k, v in params.items()
        if k not in SKIP_KEYS and str(v).strip()
    ]
    return " ".join(values)


# ─────────────────────────────────────────────
# WORKER SETUP
# ─────────────────────────────────────────────
def build_tools_for_worker(category: str):
    """Return only the tools belonging to this worker's category."""
    tools = []
    for path, description in TOOLSETS.get(resolve_category(category), []):
        script_name = path.split("/")[-1].replace(".py", "")
        args_hint = _args_hint(description)
        needs_args = "args: none" not in description.lower()
        tools.append({
            "type": "function",
            "function": {
                "name": script_name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "args": {
                            "type": "string",
                            "description": args_hint
                        }
                    },
                    "required": ["args"] if needs_args else []
                }
            }
        })
    return tools

def run_tool(tool_name: str, args: str = "") -> str:
    for entries in TOOLSETS.values():
        for path, _ in entries:
            if path.split("/")[-1].replace(".py", "") == tool_name:
                cmd = ["python", path] + (shlex.split(args) if args else [])
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                return result.stdout or result.stderr
    return f"Unknown tool: {tool_name}"

def summarise_output(output: str, max_chars: int = 600) -> str:
    output = output.strip()
    if len(output) <= max_chars:
        return output
    return output[:max_chars] + f"\n... [truncated, {len(output)} chars total]"

def run_worker(category: str, task: str) -> str:
    tools = build_tools_for_worker(category)
    if not tools:
        return f"No tools found for worker category: {category} (resolved: {resolve_category(category)})"

    worker_system = (
        f"You are a focused worker agent. You have ONE job: complete the task below using your tools.\n"
        f"IMPORTANT: Always put ALL arguments into the single 'args' field as a string, exactly as shown in the tool description.\n"
        f"Once you have the result, stop — do not call the same tool again.\n"
        f"Do not explain. Call the right tool, get the result, then output your final answer.\n\n"
        f"Reference:\n{agent_context}"
    )

    messages = [
        {"role": "system", "content": worker_system},
        {"role": "user", "content": task}
    ]

    print(f"\n  \U0001F916 Worker [{category}]: {task}")

    last_call = None   # (tool_name, args) of the most recent successful tool call
    last_result = None # last non-empty tool output

    max_steps = 8
    for step in range(max_steps):
        response = client.chat.completions.create(
            model="qwen3:1.7b",
            messages=messages,
            tools=tools,
            tool_choice="required" if step == 0 else "auto",
            extra_body={"think": False}
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            result = msg.content or (last_result if last_result else "Worker completed with no output.")
            print(f"  \u2705 Worker done: {result[:120]}")
            return result

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
            args = extract_args(tc.function.arguments)
            this_call = (tc.function.name, args)

            # Detect repeat: model is calling the exact same tool+args again after
            # already receiving a valid result — it's stuck. Return the last result.
            if this_call == last_call and last_result and not last_result.strip().startswith("ERROR"):
                print(f"  \u2705 Worker done (repeat detected): {last_result[:120]}")
                return last_result

            print(f"  \U0001F527 {tc.function.name}({args})")
            output = run_tool(tc.function.name, args)
            summary = summarise_output(output)
            print(f"  \U0001F4E4 {summary}")

            if summary.strip().startswith("Usage:"):
                summary = (
                    f"ERROR: Tool {tc.function.name} needs arguments. "
                    f"{summary.strip()} "
                    f"Put all arguments into the 'args' field exactly as the example shows."
                )
            else:
                last_call = this_call
                last_result = summary

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": summary
            })

    return last_result or "Worker reached max steps."

# ─────────────────────────────────────────────
# ORCHESTRATOR
# ─────────────────────────────────────────────
def orchestrate(user_message: str, show_thinking: bool = False):
    print(f"\n\U0001F4E8 User: {user_message}")
    print("\u2500" * 50)

    print("\U0001F9E0 Orchestrator planning...\n")
    plan_response = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": ORCHESTRATOR_PROMPT},
            {"role": "user", "content": user_message}
        ],
        extra_body={"think": show_thinking}
    )

    if show_thinking:
        thinking = getattr(plan_response.choices[0].message, "reasoning", None)
        if thinking:
            print(f"\U0001F4AD Thinking:\n{thinking}\n")

    raw_plan = plan_response.choices[0].message.content or ""
    clean_plan = raw_plan.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        plan = json.loads(clean_plan)
    except json.JSONDecodeError:
        print(f"\u274C Orchestrator returned invalid plan:\n{raw_plan}")
        return

    print(f"\U0001F4CB Plan ({len(plan)} steps):")
    for i, step in enumerate(plan):
        print(f"  {i+1}. [{step['worker']}] {step['task']}")
    print("\u2500" * 50)

    results = {}
    for i, step in enumerate(plan):
        print(f"\n\u25B6 Step {i+1}/{len(plan)}")
        task = step["task"]
        dep = step.get("depends_on", -1)
        if dep >= 0 and dep in results:
            task += f"\n\nContext from previous step:\n{results[dep]}"
        result = run_worker(step["worker"], task)
        results[i] = summarise_output(result)
        print("\u2500" * 50)

    print("\n\U0001F9E0 Orchestrator summarising...\n")
    summary_messages = [
        {"role": "system", "content": "You are a helpful assistant. Summarise what was accomplished based on the results below. Be concise."},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": f"Here are the results from each step:\n{json.dumps(results, indent=2)}"},
        {"role": "user", "content": "Please give me a brief summary of what was done and the key findings."}
    ]
    final = client.chat.completions.create(
        model="qwen3:8b",
        messages=summary_messages,
        extra_body={"think": False}
    )
    print(f"\n\u2705 Final Summary:\n{final.choices[0].message.content}")


if __name__ == "__main__":
    args = sys.argv[1:]
    show_thinking = "--think" in args
    if show_thinking:
        args.remove("--think")
    user_input = " ".join(args) or input("You: ")
    orchestrate(user_input, show_thinking=show_thinking)
