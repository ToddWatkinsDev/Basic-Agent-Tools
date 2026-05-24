import psutil

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def get_cpu_usage():
    """Returns the current CPU usage percentage."""
    return f"{psutil.cpu_percent(interval=1)}%"

if __name__ == "__main__":
    print(get_cpu_usage())
