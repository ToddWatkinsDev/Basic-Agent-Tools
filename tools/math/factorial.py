import sys
import math

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def factorial(n):
    """Returns the factorial of a non-negative integer."""
    if n < 0: return "Error: Negative input"
    return math.factorial(int(n))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(factorial(float(sys.argv[1])))
    else:
        print("Usage: python factorial.py <n>")
