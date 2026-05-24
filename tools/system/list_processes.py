import psutil

def tool(func):
    func._is_tool = True
    return func

@tool
def list_processes():
    """List top 10 running processes by memory usage."""
    try:
        procs = sorted(psutil.process_iter(['pid', 'name', 'memory_info']),
                       key=lambda p: p.info['memory_info'].rss, reverse=True)[:10]
        res = ["PID | Name | Memory"]
        for p in procs:
            mem_mb = p.info['memory_info'].rss / (1024 * 1024)
            res.append(f"{p.info['pid']} | {p.info['name']} | {mem_mb:.2f} MB")
        return "\n".join(res)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(list_processes())
