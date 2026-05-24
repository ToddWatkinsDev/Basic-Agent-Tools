import psutil

def tool(func):
    func._is_tool = True
    return func

@tool
def kill_process(pid):
    """Terminate a process by PID."""
    try:
        p = psutil.Process(int(pid))
        p.terminate()
        return f"Process {pid} terminated."
    except Exception as e:
        return f"Error killing process: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(kill_process(sys.argv[1]))
    else:
        print("Provide a PID.")
