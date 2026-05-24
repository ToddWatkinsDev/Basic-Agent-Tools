import psutil

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def get_memory_usage():
    """Returns the current RAM usage percentage."""
    return f"{psutil.virtual_memory().percent}%"

if __name__ == "__main__":
    print(get_memory_usage())
