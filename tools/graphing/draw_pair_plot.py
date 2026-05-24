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
def draw_pair_plot(dataset_path, cols_str):
    """Pair plot to visualize relationships across multiple variables. cols_str should be comma separated."""
    try:
        df = get_df(dataset_path)
        cols = cols_str.split(',')
        g = sns.pairplot(df[cols])
        g.fig.suptitle("Pair Plot of Selected Columns", y=1.02)
        plt.savefig("pair_plot.png"); plt.close()
        return "Pair plot saved to pair_plot.png"
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(draw_pair_plot(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python draw_pair_plot.py <dataset_path> \"col1,col2,col3\"")
