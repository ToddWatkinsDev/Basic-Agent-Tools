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
def draw_histogram(dataset_path, col, label):
    """Histogram to see distribution of a single variable."""
    try:
        df = get_df(dataset_path)
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {label}"); plt.xlabel(label); plt.grid(True)
        plt.savefig("histogram.png"); plt.close()
        return "Histogram saved to histogram.png"
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(draw_histogram(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else sys.argv[2]))
    else:
        print("Usage: python draw_histogram.py <dataset_path> <column> [label]")
