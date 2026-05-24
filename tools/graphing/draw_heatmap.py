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
def draw_heatmap(cols_str):
    """Correlation heatmap for multiple numeric columns. cols_str should be comma separated."""
    try:
        df = get_df()
        cols = cols_str.split(',')
        plt.figure(figsize=(12, 10))
        sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.savefig("heatmap.png")
        plt.close()
        return "Heatmap saved to heatmap.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(draw_heatmap(sys.argv[1]))
    else:
        print('Usage: python draw_heatmap.py "col1,col2,col3"')