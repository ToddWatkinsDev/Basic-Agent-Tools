import datetime

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def get_current_time():
    """Returns the current date and time in YYYY-MM-DD HH:MM:SS format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    print(get_current_time())
