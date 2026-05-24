import urllib.request
import urllib.parse
import json

def tool(func):
    func._is_tool = True
    return func

@tool
def search_web(query):
    """Search duckduckgo HTML version simply."""
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            import re
            links = re.findall(r'<a class="result__snippet[^>]+>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
            results = [re.sub(r'<[^>]+>', '', l).strip() for l in links]
            return "\n\n".join(results[:5]) if results else "No results found."
    except Exception as e:
        return f"Error searching web: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(search_web(sys.argv[1]))
