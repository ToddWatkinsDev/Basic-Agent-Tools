import urllib.request
import urllib.error

def tool(func):
    func._is_tool = True
    return func

@tool
def fetch_url(url):
    """Make an HTTP GET request and return the text/JSON response."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching URL: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(fetch_url(sys.argv[1])[:500])
