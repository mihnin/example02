# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python data analysis project featuring a full-stack Streamlit web application for sales data analysis. The project demonstrates modular architecture, comprehensive testing, and code quality practices.

**Main Application:** Interactive Streamlit web app (`app.py`) with file upload, data validation, statistical analysis, and advanced visualizations.

**Core Components:**
- Modular Streamlit application with clean architecture
- Comprehensive test suite with pytest
- Data loading with validation and error handling
- Interactive visualizations using Plotly
- Comprehensive help system
- Code quality tools integration (flake8, black, pytest-cov)

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install all dependencies
pip install streamlit plotly pandas openpyxl statsmodels pytest flake8 black pytest-cov
```

### Running the Application
```bash
# Start the Streamlit web application
streamlit run app.py
# or
python -m streamlit run app.py

# Application will be available at http://localhost:8501
```

### Testing
```bash
# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest test_analysis.py -v
python -m pytest test_compatibility.py -v

# Run tests with coverage
python -m pytest --cov=analysis --cov=data_loader --cov-report=term-missing

# Run custom functional tests
python test_refactored.py
```

### Code Quality
```bash
# Format code with black
python -m black *.py

# Check code style with flake8
python -m flake8 analysis.py --max-line-length=88 --ignore=E203,W503
python -m flake8 data_loader.py --max-line-length=88 --ignore=E203,W503

# Run all quality checks
python -m black *.py && python -m flake8 *.py --max-line-length=88 --ignore=E203,W503
```

## Architecture Overview

### Modular Design Pattern
The application follows a clean modular architecture with separation of concerns:

**`app.py`** - Main Streamlit application with UI orchestration:
- Navigation between main analysis and help pages
- File upload handling with validation feedback
- Dashboard layout with KPI metrics, charts, and data tables
- Integration of all modules through clean interfaces

**`data_loader.py`** - Data ingestion and processing layer:
- Supports Excel (.xlsx, .xls) and CSV file formats
- Automatic date column detection and normalization
- File validation with detailed error reporting
- Streamlit caching for performance (@st.cache_data)

**`analysis.py`** - Statistical analysis engine:
- KPI calculations (sessions, growth rates, averages)
- Time series analysis (moving averages, anomaly detection)
- Statistical functions (correlations, seasonal decomposition)
- Automated insight generation

**`plotting.py`** - Visualization layer using Plotly:
- Interactive time series charts with smoothing options
- Product comparison charts (bar, pie, donut)
- Heatmaps for temporal patterns
- Correlation matrices and seasonal analysis plots

**`help_page.py`** - Comprehensive help system:
- Multi-tab help interface (requirements, examples, functionality, FAQ)
- File format validation guidance
- Interactive examples with downloadable sample files

### Data Flow Architecture
1. **Input Layer**: File upload (Streamlit) → Validation (data_loader) → Error handling
2. **Processing Layer**: Raw data → Date normalization → Statistical analysis → Insight generation
3. **Presentation Layer**: Interactive charts → KPI dashboard → Data tables → Help system

### Testing Architecture
- **`test_analysis.py`**: Comprehensive pytest suite with fixtures for analysis module
- **`test_compatibility.py`**: API compatibility tests between original and refactored code
- **`test_refactored.py`**: Functional tests for refactored data loader

## Key Features

### Data Processing Pipeline
- Automatic file type detection and appropriate pandas reader selection
- Intelligent date column identification (by name patterns and content validation)
- Data quality validation with user-friendly error messages
- Support for multiple date formats and international column names

### Advanced Analytics
- Real-time KPI calculation with growth rate analysis
- Moving averages with configurable window sizes
- Anomaly detection using z-score and IQR methods
- Seasonal decomposition for time series patterns
- Correlation analysis between product sales

### Interactive Visualizations
- Plotly-based charts with zoom, pan, and hover interactions
- Configurable chart types (line, bar, pie, heatmap)
- Dynamic filtering by date ranges
- Optional data smoothing with visual indicators

### User Experience
- Two-panel navigation (Analysis / Help)
- Progressive disclosure of functionality
- Contextual help and validation feedback
- Downloadable sample files and processed data

## File Organization

```
├── app.py                     # Main Streamlit application
├── data_loader.py            # Data ingestion and validation
├── data_loader_refactored.py # Refactored version with improved architecture
├── analysis.py               # Statistical analysis functions
├── plotting.py               # Plotly visualization functions
├── help_page.py              # Help system and documentation
├── test_analysis.py          # pytest test suite for analysis module
├── test_compatibility.py     # API compatibility tests
├── test_refactored.py        # Functional tests for refactored code
├── docs/                     # Data files and Jupyter notebooks
│   ├── sample_sales_data.xlsx
│   └── пример2.ipynb
└── venv/                     # Python virtual environment
```

## Code Quality Standards

- **PEP 8 compliance** enforced via flake8
- **Comprehensive type hints** for all function signatures
- **Google-style docstrings** with Args/Returns/Raises sections
- **Modular design** with single responsibility principle
- **Error handling** with user-friendly Streamlit messaging
- **Test coverage** with pytest fixtures and edge case testing