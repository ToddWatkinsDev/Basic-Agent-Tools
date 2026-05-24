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
def draw_pair_plot(cols_str):
    """Pair plot to visualize relationships across multiple variables. cols_str should be comma separated."""
    try:
        df = get_df()
        cols = cols_str.split(',')
        g = sns.pairplot(df[cols])
        g.fig.suptitle("Pair Plot of Selected Columns", y=1.02)
        g.savefig("pair_plot.png")
        plt.close(g.fig)
        return "Pair plot saved to pair_plot.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(draw_pair_plot(sys.argv[1]))
    else:
        print('Usage: python draw_pair_plot.py "col1,col2,col3"')