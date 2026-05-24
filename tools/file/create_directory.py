import os

def tool(func):
    func._is_tool = True
    return func

@tool
def create_directory(dirpath):
    """Safely create nested directories (like mkdir -p)."""
    try:
        os.makedirs(dirpath, exist_ok=True)
        return f"Directory created: {dirpath}"
    except Exception as e:
        return f"Error creating directory: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(create_directory(sys.argv[1]))
