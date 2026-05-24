import matplotlib.pyplot as plt
import sys
import pandas as pd


def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func


def get_df():
    """Always use the cleaned dataset."""
    return pd.read_csv("clean_data.csv")


@tool
def draw_scatter_plot(x_col, y_col, x_label, y_label):
    """
    Draws a scatter plot using the cleaned dataset.
    """
    try:
        df = get_df()

        if x_col not in df.columns or y_col not in df.columns:
            return f"Error: Columns {x_col} or {y_col} not found in cleaned dataset."

        x = df[x_col]
        y = df[y_col]

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color="blue", marker="o")
        plt.title(f"{y_label} vs {x_label}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)

        output_file = "scatter_plot.png"
        plt.savefig(output_file)
        plt.close()
        return f"Plot successfully saved to {output_file}"
    except Exception as e:
        return f"Error creating plot: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) == 5:
        print(draw_scatter_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print("Usage: python draw_scatter_plot.py <x_col> <y_col> <x_label> <y_label>")
        print('Example: python draw_scatter_plot.py "Age" "Salary" "Age (Years)" "Salary ($)"')