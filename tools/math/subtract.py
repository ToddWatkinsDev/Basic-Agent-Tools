import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def subtract(a, b):
    """Returns the difference between two numbers."""
    return a - b

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(subtract(float(sys.argv[1]), float(sys.argv[2])))
    else:
        print("Usage: python subtract.py <a> <b>")
