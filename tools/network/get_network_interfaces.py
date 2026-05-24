import subprocess
import platform

def tool(func):
    func._is_tool = True
    return func

@tool
def get_network_interfaces():
    """List all local network adapters and their states."""
    try:
        cmd = 'ipconfig' if platform.system() == 'Windows' else 'ifconfig'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error getting interfaces: {e}"

if __name__ == "__main__":
    print(get_network_interfaces())
