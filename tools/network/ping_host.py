import subprocess
import platform

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def ping_host(host):
    """Checks if a host is reachable."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    return "Reachable" if subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0 else "Unreachable"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(ping_host(sys.argv[1]))
    else:
        print("Please provide a host.")
