import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def floor(a):
    """Returns the floor of a number."""
    return math.floor(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(floor(float(sys.argv[1])))
    else:
        print("Usage: python floor.py <a>")
