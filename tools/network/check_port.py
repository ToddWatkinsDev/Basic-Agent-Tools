import socket

def tool(func):
    func._is_tool = True
    return func

@tool
def check_port(host, port):
    """Check if a specific port is open on a host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex((host, int(port)))
            if result == 0:
                return f"Port {port} on {host} is OPEN"
            return f"Port {port} on {host} is CLOSED"
    except Exception as e:
        return f"Error checking port: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(check_port(sys.argv[1], sys.argv[2]))
