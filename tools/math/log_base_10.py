import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def log_base_10(a):
    """Returns the base-10 logarithm of a number."""
    if a <= 0: return "Error: Non-positive input"
    return math.log10(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(log_base_10(float(sys.argv[1])))
    else:
        print("Usage: python log_base_10.py <a>")
