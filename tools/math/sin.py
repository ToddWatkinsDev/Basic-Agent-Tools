import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def sin(a):
    """Returns the sine of a number (in radians)."""
    return math.sin(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(sin(float(sys.argv[1])))
    else:
        print("Usage: python sin.py <a>")
