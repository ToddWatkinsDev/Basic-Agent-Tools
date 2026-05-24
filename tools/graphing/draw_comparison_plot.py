import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

def get_df(dataset_path):
    """Helper to ensure we use the cleaned dataset."""
    clean_file = "clean_data.csv"
    if not os.path.exists(clean_file):
        from tools.data.clean_dataset import clean_dataset
        clean_dataset(dataset_path, clean_file)
    return pd.read_csv(clean_file)

@tool
def draw_comparison_plot(dataset_path, x_col, y_col, group_col, x_label, y_label):
    """
    Draws a scatter plot comparing two or more groups (e.g., Kite vs No-Kite).
    
    Args:
        dataset_path (str): Path to the CSV file.
        x_col (str): X-axis column.
        y_col (str): Y-axis column.
        group_col (str): Column used to color/group the data (e.g., 'source_file').
        x_label (str): Label for X axis.
        y_label (str): Label for Y axis.
    """
    try:
        df = get_df(dataset_path)
        
        if group_col not in df.columns:
            return f"Error: Grouping column {group_col} not found."

        plt.figure(figsize=(12, 8))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=group_col, palette='viridis', s=50, alpha=0.7)
        plt.title(f"{y_label} vs {x_label} by {group_col}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(title=group_col)
        plt.grid(True)
        
        output_file = "comparison_plot.png"
        plt.savefig(output_file)
        plt.close()
        return f"Comparison plot saved to {output_file}"
    except Exception as e:
        return f"Error creating comparison plot: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) == 7:
        print(draw_comparison_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))
    else:
        print("Usage: python draw_comparison_plot.py <dataset_path> <x_col> <y_col> <group_col> <x_label> <y_label>")
