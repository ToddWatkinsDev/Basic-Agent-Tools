import pandas as pd

def tool(func):
    func._is_tool = True
    return func

@tool
def convert_format(input_file, output_file):
    """Convert datasets between formats based on file extension."""
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.json'):
            df = pd.read_json(input_file)
        else:
            return "Unsupported input format."
            
        if output_file.endswith('.csv'):
            df.to_csv(output_file, index=False)
        elif output_file.endswith('.json'):
            df.to_json(output_file, orient='records')
        else:
            return "Unsupported output format."
            
        return f"Converted {input_file} to {output_file}"
    except Exception as e:
        return f"Error converting format: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(convert_format(sys.argv[1], sys.argv[2]))
