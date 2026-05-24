import pandas as pd
import sys

def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def filter_dataset(dataset_path, column, operator, value, output_path="filtered_data.csv"):
    """
    Filters a dataset based on a condition and saves the result.
    Operators: '>', '<', '==', '!='
    """
    try:
        clean_file = "clean_data.csv"
        df = pd.read_csv(clean_file if os.path.exists(clean_file) else dataset_path)
        
        if column not in df.columns:
            return f"Error: Column {column} not found."
            
        if operator == '>': filtered_df = df[df[column] > float(value)]
        elif operator == '<': filtered_df = df[df[column] < float(value)]
        elif operator == '==': filtered_df = df[df[column] == float(value)]
        elif operator == '!=': filtered_df = df[df[column] != float(value)]
        else: return "Error: Invalid operator. Use '>', '<', '==', or '!='."
        
        filtered_df.to_csv(output_path, index=False)
        return f"Filtered data saved to {output_path}. Rows: {len(filtered_df)}"
    except Exception as e:
        return f"Error filtering dataset: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) == 5:
        print(filter_dataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print("Usage: python filter_dataset.py <dataset_path> <column> <operator> <value>")
