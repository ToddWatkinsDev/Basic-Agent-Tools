import pandas as pd
import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def calculate_correlations(dataset_path):
    """
    Calculates the correlation matrix for all numeric columns in the dataset.
    """
    try:
        # Use cleaned data if available, otherwise raw
        clean_file = "clean_data.csv"
        df = pd.read_csv(clean_file if os.path.exists(clean_file) else dataset_path)
        
        numeric_df = df.select_dtypes(include=['number'])
        corr_matrix = numeric_df.corr()
        return corr_matrix.to_string()
    except Exception as e:
        return f"Error calculating correlations: {str(e)}"

if __name__ == "__main__":
    import os
    if len(sys.argv) > 1:
        print(calculate_correlations(sys.argv[1]))
    else:
        print("Usage: python calculate_correlations.py <dataset_path>")
