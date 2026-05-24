# 🤖 Agent's Toolbox: Operational Guide

Welcome! This workspace is a curated set of tools designed to give an AI agent the capabilities needed to monitor systems, manage files, diagnose networks, and perform professional-grade data science.

## 🎯 The Goal

The objective is to provide a reliable, automated pipeline for turning raw data into actionable insights while maintaining a clean and organized environment.

## 🛠️ What's in the Box?

### System Utilities (`tools/system/`)

Quick checks for the machine's health and state.

- **get_cpu_usage.py**: Monitors current CPU load.
- **get_disk_space.py**: Checks available storage.
- **get_env_variables.py**: Lists all current environment variables.
- **get_memory_usage.py**: Monitors RAM utilization.
- **get_os_info.py**: Returns operating system name and version details.
- **get_time.py**: Returns the current system time.
- **kill_process.py**: Terminates a running process by PID.
- **list_processes.py**: Lists all currently running processes.
- **run_shell_command.py**: Executes an arbitrary shell command and returns output.

### File Management (`tools/file/`)

Basic utilities for navigating and auditing the filesystem.

- **create_directory.py**: Creates a new directory at the specified path.
- **delete_file.py**: Permanently removes a file from the filesystem.
- **file_size.py**: Gets size of a specific file. **Inputs**: `File path.`
- **list_files.py**: Lists contents of a directory. **Inputs**: `Path to directory.`
- **move_file.py**: Moves or renames a file to a new location.
- **read_file.py**: Reads and returns the full contents of a file.
- **search_text.py**: Finds occurrences of a string in a file. **Inputs**: `File path, search string.`
- **write_to_file.py**: Writes or appends text content to a file.

### Network Diagnostics (`tools/network/`)

Tools to verify connectivity and identity.

- **check_port.py**: Checks whether a specific port is open on a host.
- **dns_lookup.py**: Resolves a hostname to its IP address.
- **download_file.py**: Downloads a file from a URL to a local path.
- **fetch_url.py**: Fetches the raw HTTP response from a URL.
- **get_ip_address.py**: Retrieves the local IP address.
- **get_network_interfaces.py**: Lists all available network interfaces and their addresses.
- **ping_host.py**: Checks network connectivity to a host. **Inputs**: `Hostname or IP.`

### Data Preparation (`tools/data/`)

The "Guardrail" layer. No analysis should happen without this.

- **aggregate_stats.py**: Groups data by a column and calculates a statistic for another. **Inputs**: `Dataset path, group column, target column, aggregation function.`
- **calculate_correlations.py**: Calculates the correlation matrix for numeric columns. **Inputs**: `Dataset path.`
- **clean_dataset.py**: Prepares raw CSV data for analysis. **Inputs**: `Raw CSV file path.`
- **clear_datasets.py**: Deletes the temporary cleaned dataset file.
- **convert_format.py**: Converts a dataset between supported file formats (e.g. CSV to JSON).
- **encode_categorical.py**: Encodes categorical columns as numeric values for ML compatibility.
- **filter_dataset.py**: Filters a dataset based on a numeric condition. **Inputs**: `Dataset path, column name, operator (>, <, ==, !=), and value.`
- **impute_missing.py**: Fills missing values in a dataset using a specified strategy.
- **merge_datasets.py**: Joins two datasets on a shared key column.
- **pivot_dataset.py**: Reshapes a dataset by pivoting rows into columns.
- **sample_dataset.py**: Returns a random sample of rows from a dataset.

### Graphing & Analysis (`tools/graphing/`)

Turning numbers into visuals.

- **clear_plots.py**: Deletes all generated PNG plot files in the current directory.
- **draw_bar_plot.py**: Visualizes the average value of a numeric variable across categories. **Inputs**: `Dataset path, X column, Y column, X label, Y label.`
- **draw_boxplot.py**: Visualizes quartiles and identifies outliers. **Inputs**: `Dataset path, X column, Y column, X label, Y label.`
- **draw_comparison_plot.py**: Visualizes the relationship between two variables, colored by a group. **Inputs**: `Dataset path, X column, Y column, Group column, X label, Y label.`
- **draw_heatmap.py**: Visualizes correlation between multiple numeric variables. **Inputs**: `Dataset path, Comma-separated list of columns.`
- **draw_histogram.py**: Shows the distribution of a single numeric variable. **Inputs**: `Dataset path, Column name, Label.`
- **draw_joint_plot.py**: Shows the relationship between two variables along with their marginal distributions. **Inputs**: `Dataset path, X column, Y column, X label, Y label.`
- **draw_kde_plot.py**: Visualizes the probability density of a variable. **Inputs**: `Dataset path, Column name, Label.`
- **draw_line_plot.py**: Visualizes trends over time or sequence. **Inputs**: `Dataset path, X column, Y column, X label, Y label.`
- **draw_pair_plot.py**: Creates a matrix of scatter plots for all selected numeric columns. **Inputs**: `Dataset path, Comma-separated list of columns.`
- **draw_reg_plot.py**: Visualizes the linear relationship between two variables with a regression line. **Inputs**: `Dataset path, X column, Y column, X label, Y label.`
- **draw_scatter_plot.py**: Visualizes the relationship between two numeric columns. **Inputs**: `Dataset path, X column name, Y column name, X label, Y label.`
- **draw_violin_plot.py**: Shows the distribution of quantitative data across several categories. **Inputs**: `Dataset path, X column, Y column, X label, Y label.`
- **explore_dataset.py**: Provides a high-level overview of a CSV dataset. **Inputs**: `CSV file path.`

### Math Utilities (`tools/math/`)

A comprehensive suite of mathematical and statistical functions.

- **absolute_value.py**: Returns the non-negative value of a number. **Inputs**: `Any numeric value.`
- **add.py**: Returns the sum of two numbers. **Inputs**: `Two numeric values.`
- **ceiling.py**: Rounds a number up to the nearest integer. **Inputs**: `Any numeric value.`
- **cos.py**: Calculates the cosine of an angle. **Inputs**: `Angle in radians.`
- **divide.py**: Returns the quotient of two numbers. **Inputs**: `Two numeric values.`
- **factorial.py**: Calculates the factorial of a non-negative integer. **Inputs**: `Non-negative integer.`
- **floor.py**: Rounds a number down to the nearest integer. **Inputs**: `Any numeric value.`
- **gcd.py**: Finds the greatest common divisor of two integers. **Inputs**: `Two integers.`
- **log_base_10.py**: Calculates the base-10 logarithm. **Inputs**: `Positive numeric value.`
- **mean.py**: Calculates the average of a set of numbers. **Inputs**: `Comma-separated list of numbers.`
- **median.py**: Finds the middle value in a sorted list of numbers. **Inputs**: `Comma-separated list of numbers.`
- **mode.py**: Finds the most frequent value in a list. **Inputs**: `Comma-separated list of numbers.`
- **multiply.py**: Returns the product of two numbers. **Inputs**: `Two numeric values.`
- **natural_log.py**: Calculates the natural logarithm (base e). **Inputs**: `Positive numeric value.`
- **power.py**: Returns a number raised to a specific power. **Inputs**: `Base and exponent.`
- **sin.py**: Calculates the sine of an angle. **Inputs**: `Angle in radians.`
- **square_root.py**: Calculates the square root of a number. **Inputs**: `A non-negative number.`
- **standard_deviation.py**: Calculates the sample standard deviation. **Inputs**: `Comma-separated list of numbers.`
- **subtract.py**: Returns the difference between two numbers. **Inputs**: `Two numeric values.`
- **tan.py**: Calculates the tangent of an angle. **Inputs**: `Angle in radians.`

### Web Utilities (`tools/web/`)

Tools to search and extract information from the internet.

- **scrape_html.py**: Fetches a web page and extracts its raw HTML content.
- **search_web.py**: Queries a search engine and returns a list of results.

### Machine Learning (`tools/ml/`)

Basic ML algorithms for data analysis.

- **train_linear_model.py**: Trains a linear regression model on a dataset and returns coefficients and R² score.

### Reporting (`tools/reporting/`)

Generate summaries and documents.

- **generate_pdf_report.py**: Compiles a summary of analysis results and plots into a PDF report.

### Archive Management (`tools/archive/`)

Extract compressed files.

- **extract_archive.py**: Extracts the contents of a `.zip`, `.tar.gz`, or similar archive to a target directory.

---

## 🔄 The Golden Workflow (Data Analysis)

If you are asked to analyze a CSV, **do not guess**. Follow this exact sequence:

1. **Explore**: Run `explore_dataset.py`. Find the column names and check the "Statistical Summary" for anomalies.
2. **Reset**: If you are switching to a new file, run `clear_datasets.py` first.
3. **Clean**: Run `clean_dataset.py`. This ensures the data is sane and saves it to `clean_data.csv`.
4. **Visualize**: Use any of the graphing tools. They will automatically use the cleaned data.

## 📋 Pro-Tips for the Agent

- **Environment**: Always ensure the `.venv` is active. If you see `ModuleNotFoundError`, run `pip install`.
- **State**: Remember that `clean_data.csv` is a shared state. If the user changes the dataset, you **must** clear the old one.
- **Verification**: Always check if the `.png` file was actually created before telling the user the task is done.

## 🚀 Quick Command Cheat Sheet

| Task    | Command                                                                          |
|---------|----------------------------------------------------------------------------------|
| Explore | `python tools/graphing/explore_dataset.py <file>`                                |
| Clean   | `python tools/data/clean_dataset.py <file>`                                      |
| Graph   | `python tools/graphing/draw_scatter_plot.py <file> <x_col> <y_col> <x_lab> <y_lab>` |
| Reset   | `python tools/data/clear_datasets.py`                                            |
