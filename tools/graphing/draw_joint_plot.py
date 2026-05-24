import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys


def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func


def get_df():
    """Always use the cleaned dataset."""
    return pd.read_csv("clean_data.csv")


@tool
def draw_joint_plot(x_col, y_col, x_label, y_label):
    """Joint plot showing scatter and marginal distributions."""
    try:
        df = get_df()
        g = sns.jointplot(data=df, x=x_col, y=y_col, kind="scatter")
        g.set_axis_labels(x_label, y_label)
        g.figure.suptitle(f"{y_label} vs {x_label}", y=1.02)
        g.savefig("joint_plot.png")
        plt.close(g.figure)
        return "Joint plot saved to joint_plot.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        print(draw_joint_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print("Usage: python draw_joint_plot.py <x_col> <y_col> <x_label> <y_label>")