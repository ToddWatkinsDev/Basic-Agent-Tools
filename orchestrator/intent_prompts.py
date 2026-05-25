# intent_prompts.py
# Maps user intent keywords to a specialised system prompt for the worker.
# Each entry: "intent_name": ([keyword_list], "prompt string")
# Add new intents here without touching orchestrator.py.

INTENT_PROMPTS: dict[str, tuple[list[str], str]] = {
    "system_info": (
        [
            "system info",
            "system information",
            "about this machine",
            "about my machine",
            "machine info",
            "computer info",
            "tell me about this computer",
            "what is my system",
            "full system report",
            "system overview",
            "system details",
        ],
        (
            "You are a system information agent. The user wants a FULL overview of their machine.\n"
            "You MUST call ALL of the following tools in order and report every result:\n"
            "1. get_os_info      — operating system name and version\n"
            "2. get_cpu_usage    — current CPU load percentage\n"
            "3. get_memory_usage — RAM used, available, and total\n"
            "4. get_disk_space   — disk used, free, and total\n"
            "5. get_ip_address   — local IP address\n"
            "Call each tool exactly once with an empty args string. "
            "After all five results are collected, stop and summarise everything clearly.\n"
        ),
    ),

    "network_overview": (
        [
            "network overview",
            "network info",
            "network information",
            "network status",
            "network details",
            "full network report",
            "network summary",
            "tell me about my network",
            "what is my network",
            "network diagnostics",
        ],
        (
            "You are a network diagnostics agent. The user wants a FULL overview of their network.\n"
            "You MUST call ALL of the following tools in order and report every result:\n"
            "1. get_ip_address          — local IP address of this machine\n"
            "2. get_network_interfaces  — all active network interfaces and their IPs\n"
            "3. ping_host 8.8.8.8       — check internet connectivity via Google DNS\n"
            "4. dns_lookup google.com   — verify DNS resolution is working\n"
            "Call each tool exactly once. For ping_host pass '8.8.8.8' as args. "
            "For dns_lookup pass 'google.com' as args. "
            "After all four results are collected, stop and summarise the network status clearly.\n"
        ),
    ),
}


def detect_intent_prompt(message: str) -> str | None:
    """Return a specialised worker system prompt if the message matches a known intent.
    Returns None if no intent matches (caller falls back to default prompt)."""
    lower = message.lower()
    for _, (keywords, prompt) in INTENT_PROMPTS.items():
        if any(kw in lower for kw in keywords):
            return prompt
    return None
