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
    output_dir=None,
    output_filename="clean_data.csv"
):
    """
    Cleans a dataset by removing outliers using the 3-standard-deviation rule
    and handling missing values, then saves clean_data.csv to the current
    working directory (project root) by default.

    Args:
        filepath (str): Path to the raw CSV file.
        output_dir (str): Optional directory to save the cleaned file.
                          Defaults to current working directory.
        output_filename (str): Output filename. Defaults to clean_data.csv.
    """
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape

        # Remove rows with missing values
        df = df.dropna()

        # Remove outliers using 3-standard-deviation rule
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            df = df[(df[col] >= mean - 3 * std) & (df[col] <= mean + 3 * std)]

        # Save to output_dir if specified, otherwise use cwd (project root)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_filename)
        else:
            output_path = output_filename  # resolves to cwd/clean_data.csv

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
