# merge_datasets.py

## Purpose
Merges multiple CSV files into one. Adds a 'source_file' column to track the origin of each row. Validates that all files have identical headers before merging.

## Inputs
- `file_paths_str`: A comma-separated string of file paths to the CSV files you want to merge (e.g., `"data1.csv,data2.csv"`).
- `output_path`: (Optional) The path where the merged dataset will be saved. Defaults to `"merged_data.csv"`.

## Outputs
Returns a success message indicating the number of files merged and the output file path, or an error message if the files cannot be merged (e.g. due to column mismatch).

## Usage
`python tools/data/merge_datasets.py "file1.csv,file2.csv"`
