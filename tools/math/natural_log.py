import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def natural_log(a):
    """Returns the natural logarithm of a number."""
    if a <= 0: return "Error: Non-positive input"
    return math.log(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(natural_log(float(sys.argv[1])))
    else:
        print("Usage: python natural_log.py <a>")
