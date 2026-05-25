import os, sys, shlex, json, subprocess
from openai import OpenAI

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
sys.path.insert(0, project_root)

from toolsets import TOOLSETS
from orchestrator.intent_prompts import detect_intent_prompt

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

with open("orchestrator/AGENT_PROMPT.md", "r", encoding="utf-8") as f:
    agent_context = f.read()

with open("orchestrator/ORCHESTRATOR_PROMPT.md", "r", encoding="utf-8") as f:
    ORCHESTRATOR_PROMPT = f.read()

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

# Fallback routing when the planner returns an empty plan []
FALLBACK_KEYWORDS: list[tuple[list[str], str]] = [
    (["ip address", "ip addr", "my ip"],                                         "network"),
    (["ping", "dns", "download", "fetch url", "http"],                           "network"),
    (["cpu", "memory", "ram", "disk", "storage", "time", "date",
      "clock", "os info", "processes"],                                           "system"),
    (["mean", "median", "mode", "sqrt", "calculate", "average",
      "multiply", "divide", "add", "subtract", "standard deviation"],            "math"),
    (["search", "scrape", "website"],                                             "web"),
    (["file", "folder", "directory", "read", "write", "delete"],                 "file"),
    (["csv", "dataset"],                                                          "data"),
    (["plot", "chart", "graph", "visualise", "visualize"],                       "graphing"),
]

def guess_worker(message: str) -> str:
    lower = message.lower()
    for keywords, worker in FALLBACK_KEYWORDS:
        if any(kw in lower for kw in keywords):
            return worker
    return "system"

def resolve_category(name: str) -> str:
    return WORKER_CATEGORY_MAP.get(name, name)

def _args_hint(description: str) -> str:
    for line in description.split("."):
        if "Args:" in line or "Example:" in line:
            return line.strip()
    return "Provide the required arguments as a space-separated string. Never leave empty if the tool needs input."

def extract_args(arguments_json: str) -> str:
    try:
        params = json.loads(arguments_json)
    except (json.JSONDecodeError, TypeError):
        return ""
    if "args" in params:
        return str(params["args"]).strip()
    SKIP_KEYS = {"type", "description", "required", "properties", "schema"}
    values = [
        str(v).strip()
        for k, v in params.items()
        if k not in SKIP_KEYS and str(v).strip()
    ]
    return " ".join(values)

# ─────────────────────────────────────────────
# NO-ARG TOOL DIRECT DISPATCH
# ─────────────────────────────────────────────

NO_ARG_TOOL_KEYWORDS: dict[str, list[str]] = {
    "get_ip_address":         ["ip address", "ip addr", "my ip", "local ip"],
    "get_network_interfaces": ["network interfaces", "network adapters"],
    "get_cpu_usage":          ["cpu usage", "cpu load", "processor usage", "cpu percent"],
    "get_memory_usage":       ["memory usage", "ram usage", "memory info", "ram info"],
    "get_disk_space":         ["disk space", "disk usage", "storage space", "free space"],
    "get_os_info":            ["os info", "operating system", "os name", "system info"],
    "get_time":               ["current time", "what time", "date and time", "get time",
                               "what is the time", "the time", "time is it"],
    "list_processes":         ["list processes", "running processes", "active processes"],
    "get_env_variables":      ["environment variables", "env variables", "env vars"],
}

ALL_TOOLS: dict[str, str] = {
    path.split("/")[-1].replace(".py", ""): path
    for entries in TOOLSETS.values()
    for path, _ in entries
}

def try_direct_dispatch(task: str) -> str | None:
    task_lower = task.lower()
    for tool_name, keywords in NO_ARG_TOOL_KEYWORDS.items():
        if tool_name not in ALL_TOOLS:
            continue
        if any(kw in task_lower for kw in keywords):
            print(f"  \u26a1 Direct dispatch: {tool_name}()")
            output = run_tool(tool_name, "")
            result = output.strip()
            print(f"  \U0001f4e4 {result}")
            return result
    return None


# ─────────────────────────────────────────────
# WORKER SETUP
# ─────────────────────────────────────────────

def build_tools_for_worker(category: str):
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
                        "args": {"type": "string", "description": args_hint}
                    },
                    "required": ["args"] if needs_args else []
                }
            }
        })
    return tools

def run_tool(tool_name: str, args: str = "") -> str:
    path = ALL_TOOLS.get(tool_name)
    if not path:
        return f"Unknown tool: {tool_name}"
    cmd = ["python", path] + (shlex.split(args) if args else [])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return result.stdout or result.stderr

def summarise_output(output: str, max_chars: int = 600) -> str:
    output = output.strip()
    if len(output) <= max_chars:
        return output
    return output[:max_chars] + f"\n... [truncated, {len(output)} chars total]"

def run_worker(category: str, task: str) -> str:
    direct = try_direct_dispatch(task)
    if direct is not None:
        return direct

    tools = build_tools_for_worker(category)
    if not tools:
        return f"No tools found for worker category: {category} (resolved: {resolve_category(category)})"

    intent_prompt = detect_intent_prompt(task)
    if intent_prompt:
        print(f"  \U0001f4cc Intent prompt matched for task: {task[:60]}")

    worker_system = intent_prompt or (
        "You are a focused worker agent. You have ONE job: complete the task below using your tools.\n"
        "IMPORTANT: Always put ALL arguments into the single 'args' field as a string, exactly as shown in the tool description.\n"
        "For tools that take no arguments, call them with an empty args string.\n"
        "Once you have the result, stop \u2014 do not call the same tool again.\n"
        "Do not explain. Call the right tool, get the result, then output your final answer.\n\n"
        f"Reference:\n{agent_context}"
    )

    messages = [
        {"role": "system", "content": worker_system},
        {"role": "user", "content": task}
    ]

    print(f"\n  \U0001f916 Worker [{category}]: {task}")

    last_call = None
    last_result = None
    forced_retry = False

    max_steps = 8
    for step in range(max_steps):
        tool_choice = "required" if (step == 0 or (step == 1 and forced_retry)) else "auto"

        response = client.chat.completions.create(
            model="qwen3:1.7b",
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            extra_body={"think": False}
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            if step == 0 and not forced_retry:
                forced_retry = True
                messages.append({"role": "assistant", "content": msg.content or ""})
                messages.append({
                    "role": "user",
                    "content": "You must call a tool to complete this task. Do not answer in text \u2014 use one of the tools provided right now."
                })
                continue
            result = msg.content or (last_result if last_result else "Worker completed with no output.")
            print(f"  \u2705 Worker done: {result[:120]}")
            return result

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ]
        })

        for tc in msg.tool_calls:
            args = extract_args(tc.function.arguments)
            this_call = (tc.function.name, args)

            if this_call == last_call and last_result and not last_result.strip().startswith("ERROR"):
                print(f"  \u2705 Worker done (repeat detected): {last_result[:120]}")
                return last_result

            print(f"  \U0001f527 {tc.function.name}({args})")
            output = run_tool(tc.function.name, args)
            summary = summarise_output(output)
            print(f"  \U0001f4e4 {summary}")

            if summary.strip().startswith("Usage:"):
                summary = (
                    f"ERROR: Tool {tc.function.name} needs arguments. "
                    f"{summary.strip()} "
                    f"Put all arguments into the 'args' field exactly as the example shows."
                )
            else:
                last_call = this_call
                last_result = summary

            messages.append({"role": "tool", "tool_call_id": tc.id, "content": summary})

    return last_result or "Worker reached max steps."


# ─────────────────────────────────────────────
# ORCHESTRATOR
# ─────────────────────────────────────────────

def orchestrate(user_message: str, show_thinking: bool = False):
    print(f"\n\U0001f4e8 User: {user_message}")
    print("\u2500" * 50)
    print("\U0001f9e0 Orchestrator planning...\n")

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
            print(f"\U0001f4ad Thinking:\n{thinking}\n")

    raw_plan = plan_response.choices[0].message.content or ""
    clean_plan = raw_plan.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        plan = json.loads(clean_plan)
    except json.JSONDecodeError:
        print(f"\u274c Orchestrator returned invalid plan:\n{raw_plan}")
        return

    if not plan:
        guessed = guess_worker(user_message)
        print(f"\u26a0\ufe0f  Planner returned empty plan. Falling back to [{guessed}] worker.")
        plan = [{"worker": guessed, "task": user_message, "depends_on": -1}]

    print(f"\U0001f4cb Plan ({len(plan)} steps):")
    for i, step in enumerate(plan):
        print(f"  {i+1}. [{step['worker']}] {step['task']}")
    print("\u2500" * 50)

    results = {}
    for i, step in enumerate(plan):
        print(f"\n\u25b6 Step {i+1}/{len(plan)}")
        task = step["task"]
        dep = step.get("depends_on", -1)
        if dep >= 0 and dep in results:
            task += f"\n\nContext from previous step:\n{results[dep]}"
        result = run_worker(step["worker"], task)
        results[i] = summarise_output(result)
        print("\u2500" * 50)

    print("\n\U0001f9e0 Orchestrator summarising...\n")
    summary_messages = [
        {"role": "system", "content": "Summarise what was accomplished. Be concise."},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": f"Results:\n{json.dumps(results, indent=2)}"},
        {"role": "user", "content": "Brief summary of what was done and key findings."}
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
