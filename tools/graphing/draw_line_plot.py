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
def draw_line_plot(x_col, y_col, x_label, y_label):
    """Line plot for trends over time/sequence."""
    try:
        df = get_df()
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x=x_col, y=y_col)
        plt.title(f"{y_label} vs {x_label}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.savefig("line_plot.png")
        plt.close()
        return "Line plot saved to line_plot.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        print(draw_line_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print("Usage: python draw_line_plot.py <x_col> <y_col> <x_label> <y_label>")