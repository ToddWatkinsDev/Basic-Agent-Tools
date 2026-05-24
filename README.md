# 🤖 Agent Tools Framework

Welcome to the **Agent Tools Framework**! This project provides a sandboxed, modular environment designed to give an AI Agent a robust set of real-world capabilities. It allows an AI to safely execute system checks, manage files, diagnose networks, and perform automated, professional-grade data science.

## 🎯 What is this project?
Think of this repository as a "toolbelt" for an AI. An LLM (Large Language Model) on its own can only write text. But by giving it access to this workspace, the AI can:
*   Monitor your PC's health (CPU, RAM, Disk).
*   Read, search, and manage your local files.
*   Clean messy CSV datasets automatically.
*   Generate complex statistical visualizations (scatter plots, heatmaps, etc.) directly on your machine.

## 🏗️ How it Works
To ensure the AI knows exactly how to use its tools without getting confused, the project is split into two perfectly mirrored halves:

1.  **`tools/`**: This is where the actual Python code lives. If the AI wants to draw a graph, it runs a script from here.
2.  **`context/`**: This is the "API Manual" for the AI. For every Python script in `tools/`, there is a matching Markdown (`.md`) file here. The AI reads these files to learn what the tool does, what arguments it requires, and what it outputs.

The `AGENT_CONTEXT.md` file serves as the main entry point and workflow guide for the AI Agent.

---

## 🧼 The Data Science "Guardrails"
One of the core features of this framework is its strict, automated data pipeline. AI agents are prone to hallucinating data or failing on messy datasets. To prevent this, we enforce a strict workflow:

1.  **Explore**: The AI first runs `explore_dataset.py` to understand the CSV columns.
2.  **Clean**: Before any analysis is allowed, the AI must run `clean_dataset.py`. This script automatically removes missing values (NaNs) and drops extreme outliers (3-standard deviations), saving the safe result to `clean_data.csv`.
3.  **Analyze**: Graphing tools (like `draw_scatter_plot.py`) are hardcoded to look for `clean_data.csv`. If the AI tries to graph raw data without cleaning it first, the tool will automatically trigger the cleaning process for them.

---

## 🛠️ For Developers: Building New Tools

If you want to add a new capability to the AI's toolbelt, follow these guidelines:

### 1. Create the Tool Logic (`tools/`)
Create a `.py` file in the appropriate category folder (e.g., `tools/system/my_tool.py`). Every tool must use the custom `@tool` decorator:
```python
def tool(func):
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func

@tool
def my_function():
    """Description of what this tool does."""
    return "Result"
```
*Note: Always include an `if __name__ == "__main__":` block so the tool can be run directly from the terminal.*

### 2. Create the AI Documentation (`context/`)
Create a corresponding `.md` file in the `context/` directory following the exact same folder structure (e.g., `context/system/my_tool.md`). You must describe the **Purpose**, **Inputs**, and **Outputs**.

### 3. Register the Tool (`toolsets.py`)
Add the relative path of your new `.py` file to the `TOOLSETS` dictionary inside `toolsets.py`. If it is not listed here, the AI will not know it exists.

---

## 🚀 How to Run Manually
While these tools are designed for an AI, you can run any of them yourself via the command line:

```bash
# Check the time
python tools/system/get_time.py

# Clean a dataset
python tools/data/clean_dataset.py path/to/your/data.csv

# Draw a scatter plot
python tools/graphing/draw_scatter_plot.py path/to/your/data.csv column_X column_Y "X Label" "Y Label"
```
