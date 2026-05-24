import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(multiply(float(sys.argv[1]), float(sys.argv[2])))
    else:
        print("Usage: python multiply.py <a> <b>")
