import os

def tool(func):
    func._is_tool = True
    return func

@tool
def delete_file(filepath):
    """Safely delete a specific file."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return f"Deleted {filepath}"
        return f"File {filepath} not found."
    except Exception as e:
        return f"Error deleting file: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(delete_file(sys.argv[1]))
