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
def draw_kde_plot(col, label=None):
    """Kernel Density Estimate plot for smooth distribution."""
    try:
        df = get_df()
        if label is None:
            label = col

        plt.figure(figsize=(10, 6))
        sns.kdeplot(df[col], fill=True)
        plt.title(f"KDE of {label}")
        plt.xlabel(label)
        plt.grid(True)
        plt.savefig("kde_plot.png")
        plt.close()
        return "KDE plot saved to kde_plot.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(draw_kde_plot(sys.argv[1]))
    elif len(sys.argv) == 3:
        print(draw_kde_plot(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python draw_kde_plot.py <column> [label]")