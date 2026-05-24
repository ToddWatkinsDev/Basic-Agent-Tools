import sys
import statistics

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def mode(numbers_str):
    """Returns the mode of a comma-separated list of numbers."""
    try:
        nums = [float(x) for x in numbers_str.split(',')]
        return statistics.mode(nums)
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(mode(sys.argv[1]))
    else:
        print("Usage: python mode.py \"1,2,3\"")
