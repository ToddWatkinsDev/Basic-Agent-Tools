import shutil

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def get_disk_space():
    """Returns the available disk space on the root directory in GB."""
    total, used, free = shutil.disk_usage("/")
    return f"{free // (2**30)} GB"

if __name__ == "__main__":
    print(get_disk_space())
