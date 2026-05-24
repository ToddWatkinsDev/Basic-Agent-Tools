import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def absolute_value(a):
    """Returns the absolute value of a number."""
    return abs(a)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(absolute_value(float(sys.argv[1])))
    else:
        print("Usage: python absolute_value.py <a>")
