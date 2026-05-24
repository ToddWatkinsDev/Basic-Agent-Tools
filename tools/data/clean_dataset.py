import pandas as pd
import sys
import os


def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func


@tool
def clean_dataset(
    filepath,
    output_dir=r"C:\Users\jerse\OneDrive\Documenten\Agent Tools\tools\graphing",
    output_filename="clean_data.csv"
):
    """
    Cleans a dataset by removing outliers using the 3-standard-deviation rule
    and handling missing values, then saves it to the graphing folder.
    """
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape

        df = df.dropna()

        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            df = df[(df[col] >= mean - 3 * std) & (df[col] <= mean + 3 * std)]

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)

        df.to_csv(output_path, index=False)

        final_shape = df.shape
        return (
            f"Dataset cleaned. Rows reduced from {initial_shape[0]} to {final_shape[0]}. "
            f"Saved to {output_path}"
        )
    except Exception as e:
        return f"Error cleaning dataset: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(clean_dataset(sys.argv[1]))
    else:
        print("Usage: python clean_dataset.py <filepath.csv>")