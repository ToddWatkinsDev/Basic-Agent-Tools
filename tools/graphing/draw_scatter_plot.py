import matplotlib.pyplot as plt
import sys
import pandas as pd
import os
from tools.data.clean_dataset import clean_dataset

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def draw_scatter_plot(dataset_path, x_col, y_col, x_label, y_label):
    """
    Draws a scatter plot using a dataset file and specified columns.
    Automatically cleans the data if not already cleaned.
    
    Args:
        dataset_path (str): Path to the CSV file.
        x_col (str): Name of the column for the x-axis.
        y_col (str): Name of the column for the y-axis.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
    """
    try:
        # AUTOMATIC CLEANING MECHANISM
        clean_file = "clean_data.csv"
        if not os.path.exists(clean_file):
            print(f"Cleaned data not found. Automatically cleaning {dataset_path}...")
            clean_result = clean_dataset(dataset_path, clean_file)
            print(clean_result)
        
        # Use the cleaned file
        df = pd.read_csv(clean_file)
        
        if x_col not in df.columns or y_col not in df.columns:
            return f"Error: Columns {x_col} or {y_col} not found in cleaned dataset."

        x = df[x_col]
        y = df[y_col]

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='blue', marker='o')
        plt.title(f"{y_label} vs {x_label}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        
        output_file = "scatter_plot.png"
        plt.savefig(output_file)
        plt.close()
        return f"Plot successfully saved to {output_file}"
    except Exception as e:
        return f"Error creating plot: {str(e)}"

if __name__ == "__main__":
    # Usage: python draw_scatter_plot.py <dataset_path> <x_col> <y_col> <x_label> <y_label>
    if len(sys.argv) == 6:
        print(draw_scatter_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    else:
        print("Usage: python draw_scatter_plot.py <dataset_path> <x_col> <y_col> <x_label> <y_label>")
        print("Example: python draw_scatter_plot.py \"data.csv\" \"Age\" \"Salary\" \"Age (Years)\" \"Salary ($)\"")
