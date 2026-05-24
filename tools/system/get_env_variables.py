import os

def tool(func):
    func._is_tool = True
    return func

@tool
def get_env_variables(var_name):
    """Read a specific environment variable."""
    return os.environ.get(var_name, "Variable not found.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(get_env_variables(sys.argv[1]))
    else:
        print("Provide a variable name.")
