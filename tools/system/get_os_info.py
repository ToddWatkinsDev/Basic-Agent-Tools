import platform

def tool(func):
    func._is_tool = True
    return func

@tool
def get_os_info():
    """Fetch OS version and architecture."""
    return f"System: {platform.system()} {platform.release()} ({platform.machine()})\nVersion: {platform.version()}"

if __name__ == "__main__":
    print(get_os_info())
