import pandas as pd
import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def explore_dataset(filepath):
    """
    Explores a dataset (CSV) and provides structural and statistical information.
    
    Args:
        filepath (str): Path to the CSV file.
    """
    try:
        df = pd.read_csv(filepath)
        
        # 1. Column Headings
        columns = df.columns.tolist()
        
        # 2. Example Rows (First 5)
        head = df.head(5).to_string()
        
        # 3. Statistical Summary
        # We only calculate stats for numeric columns
        stats = df.describe().to_string()
        
        # Calculate Mode separately as describe() doesn't include it
        mode_info = ""
        numeric_cols = df.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            mode_df = df[numeric_cols].mode().iloc[0]
            mode_info = f"\n\nModes:\n{mode_df.to_string()}"

        result = (
            f"--- Dataset Exploration: {filepath} ---\n\n"
            f"Columns:\n{columns}\n\n"
            f"First 5 Rows:\n{head}\n\n"
            f"Statistical Summary (Min, Max, Mean, Std, etc.):\n{stats}"
            f"{mode_info}"
        )
        return result
    except Exception as e:
        return f"Error exploring dataset: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(explore_dataset(sys.argv[1]))
    else:
        print("Usage: python explore_dataset.py <filepath.csv>")
