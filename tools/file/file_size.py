import os

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def get_file_size(filepath):
    """Returns the size of a specific file in bytes."""
    try:
        return f"{os.path.getsize(filepath)} bytes"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(get_file_size(sys.argv[1]))
    else:
        print("Please provide a file path.")
