def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def search_text(filepath, search_string):
    """Searches for a string within a file and returns line numbers."""
    results = []
    try:
        with open(filepath, 'r') as f:
            for i, line in enumerate(f, 1):
                if search_string in line:
                    results.append(i)
        return results
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(search_text(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python search_text.py <file> <string>")
