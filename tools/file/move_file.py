import shutil

def tool(func):
    func._is_tool = True
    return func

@tool
def move_file(src, dest):
    """Move or rename files and directories."""
    try:
        shutil.move(src, dest)
        return f"Moved {src} to {dest}"
    except Exception as e:
        return f"Error moving file: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(move_file(sys.argv[1], sys.argv[2]))
