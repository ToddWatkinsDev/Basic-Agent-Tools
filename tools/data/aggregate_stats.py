import pandas as pd
import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def aggregate_stats(dataset_path, group_col, target_col, agg_func="mean"):
    """
    Groups data by a column and calculates a statistic for another column.
    agg_func options: 'mean', 'median', 'std', 'sum', 'count'
    """
    try:
        clean_file = "clean_data.csv"
        df = pd.read_csv(clean_file if os.path.exists(clean_file) else dataset_path)
        
        if group_col not in df.columns or target_col not in df.columns:
            return "Error: Columns not found."
            
        result = df.groupby(group_col)[target_col].agg(agg_func)
        return result.to_string()
    except Exception as e:
        return f"Error aggregating stats: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) == 4:
        print(aggregate_stats(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print("Usage: python aggregate_stats.py <dataset_path> <group_col> <target_col>")
