import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def gcd(a, b):
    """Returns the greatest common divisor of two integers."""
    return math.gcd(int(a), int(b))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(gcd(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python gcd.py <a> <b>")
