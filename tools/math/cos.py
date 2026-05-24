import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def cos(a):
    """Returns the cosine of a number (in radians)."""
    return math.cos(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(cos(float(sys.argv[1])))
    else:
        print("Usage: python cos.py <a>")
