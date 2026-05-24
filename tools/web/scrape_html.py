import urllib.request
import re

def tool(func):
    func._is_tool = True
    return func

@tool
def scrape_html(url):
    """Extract readable text from a webpage URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8', errors='ignore')
            text = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.IGNORECASE|re.DOTALL)
            text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE|re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:2000] # Return first 2000 chars to avoid overload
    except Exception as e:
        return f"Error scraping HTML: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(scrape_html(sys.argv[1]))
