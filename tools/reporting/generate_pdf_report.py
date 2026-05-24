import os

def tool(func):
    func._is_tool = True
    return func

@tool
def generate_pdf_report(text_summary, output_name='report.pdf'):
    """Generate a Markdown report simulating PDF structure."""
    try:
        report_content = f"# Generated Report\n\n{text_summary}\n\n## Plots Included\n"
        plots = [f for f in os.listdir('.') if f.endswith('.png')]
        for p in plots:
            report_content += f"![{p}]({p})\n"
            
        with open(output_name.replace('.pdf', '.md'), 'w') as f:
            f.write(report_content)
        return f"Generated report as {output_name.replace('.pdf', '.md')} (Markdown simulation of PDF)"
    except Exception as e:
        return f"Error generating report: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(generate_pdf_report(sys.argv[1]))
