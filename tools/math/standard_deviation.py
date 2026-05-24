import sys
import statistics

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def standard_deviation(numbers_str):
    """Returns the sample standard deviation of a comma-separated list of numbers."""
    try:
        nums = [float(x) for x in numbers_str.split(',')]
        return statistics.stdev(nums)
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(standard_deviation(sys.argv[1]))
    else:
        print("Usage: python standard_deviation.py \"1,2,3\"")
