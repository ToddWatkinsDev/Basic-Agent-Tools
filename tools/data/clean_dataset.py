import pandas as pd
import sys
import os

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def clean_dataset(filepath, output_path="clean_data.csv"):
    """
    Cleans a dataset by removing outliers using the 3-Standard Deviation rule 
    and handling missing values.
    
    Args:
        filepath (str): Path to the raw CSV file.
        output_path (str): Path to save the cleaned CSV.
    """
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape
        
        # 1. Handle Missing Values (Drop rows with any NaN)
        df = df.dropna()
        
        # 2. Remove Outliers using 3-Standard Deviation rule
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            # Keep only rows within 3 standard deviations
            df = df[(df[col] >= mean - 3 * std) & (df[col] <= mean + 3 * std)]
        
        df.to_csv(output_path, index=False)
        
        final_shape = df.shape
        return f"Dataset cleaned. Rows reduced from {initial_shape[0]} to {final_shape[0]}. Saved to {output_path}"
    except Exception as e:
        return f"Error cleaning dataset: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(clean_dataset(sys.argv[1]))
    else:
        print("Usage: python clean_dataset.py <filepath.csv>")
