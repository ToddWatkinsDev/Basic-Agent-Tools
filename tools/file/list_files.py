import os

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def list_files(path="."):
    """Lists files in the specified directory."""
    try:
        return os.listdir(path)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print(list_files())
