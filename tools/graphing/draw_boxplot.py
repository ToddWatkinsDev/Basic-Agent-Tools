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
def draw_boxplot(dataset_path, x_col, y_col, x_label, y_label):
    """Box plot to visualize quartiles and outliers."""
    try:
        df = get_df(dataset_path)
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(f"{y_label} by {x_label}"); plt.xlabel(x_label); plt.ylabel(y_label)
        plt.savefig("boxplot.png"); plt.close()
        return "Boxplot saved to boxplot.png"
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 6:
        print(draw_boxplot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    else:
        print("Usage: python draw_boxplot.py <dataset_path> <x_col> <y_col> <x_label> <y_label>")
