import urllib.request

def tool(func):
    func._is_tool = True
    return func

@tool
def download_file(url, dest):
    """Download a file from the internet directly to local workspace."""
    try:
        urllib.request.urlretrieve(url, dest)
        return f"Downloaded {url} to {dest}"
    except Exception as e:
        return f"Error downloading file: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(download_file(sys.argv[1], sys.argv[2]))
