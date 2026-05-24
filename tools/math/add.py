import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(add(float(sys.argv[1]), float(sys.argv[2])))
    else:
        print("Usage: python add.py <a1> <b>")
