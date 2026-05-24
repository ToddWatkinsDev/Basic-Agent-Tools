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
def draw_reg_plot(dataset_path, x_col, y_col, x_label, y_label):
    """Regression plot to see the linear trend."""
    try:
        df = get_df(dataset_path)
        plt.figure(figsize=(10, 6))
        sns.regplot(data=df, x=x_col, y=y_col)
        plt.title(f"Regression: {y_label} vs {x_label}"); plt.xlabel(x_label); plt.ylabel(y_label)
        plt.savefig("reg_plot.png"); plt.close()
        return "Regression plot saved to reg_plot.png"
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 6:
        print(draw_reg_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    else:
        print("Usage: python draw_reg_plot.py <dataset_path> <x_col> <y_col> <x_label> <y_label>")
