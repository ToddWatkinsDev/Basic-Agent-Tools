import pandas as pd

def tool(func):
    func._is_tool = True
    return func

@tool
def pivot_dataset(input_file, index_col, val_col, func='sum'):
    """Reshape the dataset into a pivot table to summarize data."""
    try:
        df = pd.read_csv(input_file)
        pivot = pd.pivot_table(df, values=val_col, index=index_col, aggfunc=func)
        pivot.to_csv('pivot_result.csv')
        return f"Pivot table created at pivot_result.csv"
    except Exception as e:
        return f"Error pivoting dataset: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 4:
        print(pivot_dataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
