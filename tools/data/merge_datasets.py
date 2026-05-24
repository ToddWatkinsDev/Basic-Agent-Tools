import pandas as pd
import sys
import os

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def merge_datasets(file_paths_str, output_path="merged_data.csv"):
    """
    Merges multiple CSV files into one. 
    Adds a 'source_file' column to track origin.
    Validates that all files have the same headers.
    """
    try:
        paths = file_paths_str.split(',')
        all_dfs = []
        
        # Read first file to get reference headers
        first_df = pd.read_csv(paths[0])
        ref_cols = set(first_df.columns)
        
        for path in paths:
            df = pd.read_csv(path)
            if set(df.columns) != ref_cols:
                return f"Error: Column mismatch in file {path}. Headers must be identical."
            
            # Add source file column
            df['source_file'] = os.path.basename(path)
            all_dfs.append(df)
            
        merged_df = pd.concat(all_dfs, ignore_index=True)
        merged_df.to_csv(output_path, index=False)
        return f"Successfully merged {len(paths)} files into {output_path}"
    except Exception as e:
        return f"Error merging datasets: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(merge_datasets(sys.argv[1]))
    else:
        print("Usage: python merge_datasets.py \"file1.csv,file2.csv\"")
