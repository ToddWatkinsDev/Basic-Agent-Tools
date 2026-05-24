import os

def tool(func):
    func._is_tool = True
    return func

@tool
def write_to_file(filepath, content, append=False):
    """Create a new file or append text to an existing one."""
    mode = 'a' if append else 'w'
    try:
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(write_to_file(sys.argv[1], sys.argv[2]))
