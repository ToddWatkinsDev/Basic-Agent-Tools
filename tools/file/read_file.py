import os

def tool(func):
    func._is_tool = True
    return func

@tool
def read_file(filepath):
    """Read the contents of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(read_file(sys.argv[1]))
