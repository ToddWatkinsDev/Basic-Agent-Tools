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
def draw_reg_plot(x_col, y_col, x_label, y_label):
    """Regression plot to see the linear trend."""
    try:
        df = get_df()
        plt.figure(figsize=(10, 6))
        sns.regplot(data=df, x=x_col, y=y_col)
        plt.title(f"Regression: {y_label} vs {x_label}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig("reg_plot.png")
        plt.close()
        return "Regression plot saved to reg_plot.png"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        print(draw_reg_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print("Usage: python draw_reg_plot.py <x_col> <y_col> <x_label> <y_label>")