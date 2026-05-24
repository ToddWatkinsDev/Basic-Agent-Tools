import os

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def clear_datasets():
    """
    Removes the temporary cleaned dataset file to ensure the next 
    dataset is processed fresh.
    """
    try:
        target_file = "clean_data.csv"
        if os.path.exists(target_file):
            os.remove(target_file)
            return f"Successfully removed {target_file}."
        else:
            return "No cleaned dataset file found to remove."
    except Exception as e:
        return f"Error clearing datasets: {str(e)}"

if __name__ == "__main__":
    print(clear_datasets())
