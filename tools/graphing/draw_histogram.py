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
def draw_histogram(col, label=None):
    """Histogram to see distribution of a single variable."""
    try:
        df = get_df()
        if label is None:
            label = col

        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {label}")
        plt.xlabel(label)
        plt.grid(True)
        plt.savefig("histogram.png")
        plt.close()
        return "Histogram saved to histogram.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(draw_histogram(sys.argv[1]))
    elif len(sys.argv) == 3:
        print(draw_histogram(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python draw_histogram.py <column> [label]")