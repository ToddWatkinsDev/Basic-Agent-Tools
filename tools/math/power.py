import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def power(a, b):
    """Returns a raised to the power of b."""
    return math.pow(a, b)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(power(float(sys.argv[1]), float(sys.argv[2])))
    else:
        print("Usage: python power.py <a> <b>")
