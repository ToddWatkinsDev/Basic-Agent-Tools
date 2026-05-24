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
def draw_heatmap(dataset_path, cols_str):
    """Correlation heatmap for multiple numeric columns. cols_str should be comma separated."""
    try:
        df = get_df(dataset_path)
        cols = cols_str.split(',')
        plt.figure(figsize=(12, 10))
        sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Heatmap"); plt.savefig("heatmap.png"); plt.close()
        return "Heatmap saved to heatmap.png"
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(draw_heatmap(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python draw_heatmap.py <dataset_path> \"col1,col2,col3\"")
