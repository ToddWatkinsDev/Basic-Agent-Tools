import pandas as pd

def tool(func):
    func._is_tool = True
    return func

@tool
def encode_categorical(input_file, column):
    """Convert text categories into numeric IDs."""
    try:
        df = pd.read_csv(input_file)
        df[column] = df[column].astype('category').cat.codes
        df.to_csv(input_file, index=False)
        return f"Encoded categorical column: {column}"
    except Exception as e:
        return f"Error encoding dataset: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(encode_categorical(sys.argv[1], sys.argv[2]))
