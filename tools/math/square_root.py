import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def square_root(a):
    """Returns the square root of a number."""
    if a < 0: return "Error: Negative input"
    return math.sqrt(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(square_root(float(sys.argv[1])))
    else:
        print("Usage: python square_root.py <a>")
