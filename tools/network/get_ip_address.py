import socket

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def get_ip_address():
    """Returns the local IP address."""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print(get_ip_address())
