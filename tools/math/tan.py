import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def tan(a):
    """Returns the tangent of a number (in radians)."""
    return math.tan(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(tan(float(sys.argv[1])))
    else:
        print("Usage: python tan.py <a>")
