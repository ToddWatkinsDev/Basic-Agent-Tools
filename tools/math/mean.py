import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def mean(numbers_str):
    """Returns the mean of a comma-separated list of numbers."""
    try:
        nums = [float(x) for x in numbers_str.split(',')]
        return sum(nums) / len(nums)
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(mean(sys.argv[1]))
    else:
        print("Usage: python mean.py \"1,2,3\"")
