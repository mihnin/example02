# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python data analysis project focused on sales data analysis. The repository contains:
- Jupyter notebook for data analysis (`docs/пример2.ipynb`)
- Sample sales data Excel file (`docs/sample_sales_data.xlsx`)
- Python virtual environment (`venv/`)

## Environment Setup

The project uses a Python virtual environment for dependency management:

### Activate virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### Core Dependencies (inferred from notebook):
- pandas: For data loading and manipulation
- matplotlib: For data visualization

To install dependencies when working with the notebook:
```bash
pip install pandas matplotlib openpyxl
```

## Development Workflow

### Working with Jupyter Notebooks:
- Main analysis notebook: `docs/пример2.ipynb`
- Contains sales data analysis with statistical summaries and visualizations
- Uses Russian language for documentation and variable names

### Data Analysis Structure:
The notebook follows this analysis pattern:
1. Data loading from Excel files using pandas
2. Data exploration and statistical analysis
3. Trend analysis and pattern identification
4. Data visualization with matplotlib
5. Comprehensive reporting in both Russian and English

## File Structure

- `docs/` - Contains notebooks and data files
- `venv/` - Python virtual environment
- `README.md` - Basic project description in Russian
- `LICENSE` - Project license

## Development Notes

- The project uses Russian language for documentation, comments, and variable names
- Excel files are the primary data source format
- Analysis focuses on time series sales data with multiple products
- Statistical analysis includes descriptive statistics, trend analysis, and seasonal pattern identification