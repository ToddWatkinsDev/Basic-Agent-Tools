import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def ceiling(a):
    """Returns the ceiling of a number."""
    return math.ceil(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(ceiling(float(sys.argv[1])))
    else:
        print("Usage: python ceiling.py <a>")
