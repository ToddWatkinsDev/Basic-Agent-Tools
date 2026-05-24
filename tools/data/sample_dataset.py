import pandas as pd

def tool(func):
    func._is_tool = True
    return func

@tool
def sample_dataset(input_file, n, output_file):
    """Extract a random subset of rows from a dataset."""
    try:
        df = pd.read_csv(input_file)
        sample = df.sample(n=int(n))
        sample.to_csv(output_file, index=False)
        return f"Sampled {n} rows from {input_file} to {output_file}"
    except Exception as e:
        return f"Error sampling dataset: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        print(sample_dataset(sys.argv[1], sys.argv[2], sys.argv[3]))
