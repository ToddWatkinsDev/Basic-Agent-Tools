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
def draw_boxplot(x_col, y_col, x_label, y_label):
    """Box plot to visualize quartiles and outliers."""
    try:
        df = get_df()
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(f"{y_label} by {x_label}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig("boxplot.png")
        plt.close()
        return "Boxplot saved to boxplot.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        print(draw_boxplot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print("Usage: python draw_boxplot.py <x_col> <y_col> <x_label> <y_label>")