import subprocess

def tool(func):
    func._is_tool = True
    return func

@tool
def run_shell_command(command):
    """Execute a raw terminal command and return output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(run_shell_command(sys.argv[1]))
    else:
        print("Provide a command.")
