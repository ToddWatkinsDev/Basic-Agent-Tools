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
def draw_comparison_plot(x_col, y_col, group_col, x_label, y_label):
    """
    Draws a scatter plot comparing two or more groups.
    """
    try:
        df = get_df()

        if group_col not in df.columns:
            return f"Error: Grouping column {group_col} not found."

        plt.figure(figsize=(12, 8))
        sns.scatterplot(
            data=df,
            x=x_col,
            y=y_col,
            hue=group_col,
            palette="viridis",
            s=50,
            alpha=0.7
        )
        plt.title(f"{y_label} vs {x_label} by {group_col}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(title=group_col)
        plt.grid(True)

        output_file = "comparison_plot.png"
        plt.savefig(output_file)
        plt.close()
        return f"Comparison plot saved to {output_file}"
    except Exception as e:
        return f"Error creating comparison plot: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) == 6:
        print(draw_comparison_plot(
            sys.argv[1],
            sys.argv[2],
            sys.argv[3],
            sys.argv[4],
            sys.argv[5]
        ))
    else:
        print("Usage: python draw_comparison_plot.py <x_col> <y_col> <group_col> <x_label> <y_label>")