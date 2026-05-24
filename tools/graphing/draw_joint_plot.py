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
def draw_joint_plot(dataset_path, x_col, y_col, x_label, y_label):
    """Joint plot showing scatter and marginal distributions."""
    try:
        df = get_df(dataset_path)
        g = sns.jointplot(data=df, x=x_col, y=y_col, kind="scatter")
        g.set_axis_labels(x_label, y_label).fig.suptitle(f"{y_label} vs {x_label}", y=1.02)
        plt.savefig("joint_plot.png"); plt.close()
        return "Joint plot saved to joint_plot.png"
    except Exception as e: return str(e)

if __name__ == "__main__":
    if len(sys.argv) == 6:
        print(draw_joint_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    else:
        print("Usage: python draw_joint_plot.py <dataset_path> <x_col> <y_col> <x_label> <y_label>")
