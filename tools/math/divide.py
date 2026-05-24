import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def divide(a, b):
    """Returns the quotient of two numbers."""
    if b == 0: return "Error: Division by zero"
    return a / b

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(divide(float(sys.argv[1]), float(sys.argv[2])))
    else:
        print("Usage: python divide.py <a> <b>")
