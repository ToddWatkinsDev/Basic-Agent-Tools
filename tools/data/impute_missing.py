import pandas as pd

def tool(func):
    func._is_tool = True
    return func

@tool
def impute_missing(input_file, column, strategy):
    """Fill NaNs in a column with mean, median, or mode."""
    try:
        df = pd.read_csv(input_file)
        if strategy == 'mean':
            df[column] = df[column].fillna(df[column].mean())
        elif strategy == 'median':
            df[column] = df[column].fillna(df[column].median())
        elif strategy == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0])
        else:
            return "Invalid strategy."
            
        df.to_csv(input_file, index=False)
        return f"Imputed missing values in {column} using {strategy}."
    except Exception as e:
        return f"Error imputing dataset: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        print(impute_missing(sys.argv[1], sys.argv[2], sys.argv[3]))
