import socket

def tool(func):
    func._is_tool = True
    return func

@tool
def dns_lookup(domain):
    """Resolve a domain name to its IP addresses."""
    try:
        ip = socket.gethostbyname(domain)
        return f"Domain {domain} resolves to {ip}"
    except Exception as e:
        return f"Error looking up DNS: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(dns_lookup(sys.argv[1]))
