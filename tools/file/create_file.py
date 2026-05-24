import os
import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def create_file(filepath, content=""):
    """
    Creates a new file at the specified path.
    If the file already exists, it will not be overwritten.
    Optionally writes initial content to the file.

    Args:
        filepath (str): Path to the file to create.
        content (str): Optional initial content to write (default: empty).
    """
    try:
        # Create any missing parent directories
        parent = os.path.dirname(filepath)
        if parent:
            os.makedirs(parent, exist_ok=True)

        if os.path.exists(filepath):
            return f"File already exists: {filepath}"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        if content:
            return f"File created with content: {filepath}"
        else:
            return f"Empty file created: {filepath}"

    except Exception as e:
        return f"Error creating file: {e}"

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
        content = sys.argv[2] if len(sys.argv) > 2 else ""
        print(create_file(filepath, content))
    else:
        print("Usage: python create_file.py <filepath> [initial_content]")
        print("Example: python create_file.py output/notes.txt \"Hello World\"")
