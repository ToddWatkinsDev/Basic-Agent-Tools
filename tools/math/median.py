import sys
import statistics

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def median(numbers_str):
    """Returns the median of a comma-separated list of numbers."""
    try:
        nums = [float(x) for x in numbers_str.split(',')]
        return statistics.median(nums)
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(median(sys.argv[1]))
    else:
        print("Usage: python median.py \"1,2,3\"")
