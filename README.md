# 📊 Website Traffic Analyzer

**🌐 Live Demo:** https://example02.streamlit.app/

*[Русская версия](README-ru.md) | [English version](README.md)*

---

## 🎯 Overview

**Website Traffic Analyzer** is a comprehensive business intelligence tool designed for sales and traffic data analysis. Built with Streamlit, this application provides powerful analytics capabilities with an intuitive web interface.

### 🌟 Key Features

- **📈 Sales & Traffic Analysis** - Time series data processing and analysis
- **📊 Interactive Visualizations** - Charts, heatmaps, correlation matrices
- **🎯 KPI Dashboard** - Automated calculation of key performance indicators
- **🔍 Anomaly Detection** - Identify unusual patterns and outliers
- **📋 Automated Insights** - AI-generated conclusions and recommendations
- **🐳 Docker Support** - Containerized deployment with CI/CD pipeline

### 🏢 Business Applications

- **E-commerce:** Product sales analysis, conversion monitoring
- **Web Analytics:** Traffic analysis, user behavior insights
- **Marketing:** Campaign ROI, channel performance tracking
- **Business Intelligence:** Data-driven decision making

---

## 🚀 Quick Start

### 🌐 Online Demo

Simply visit: **https://example02.streamlit.app/**

### 💻 Local Installation

#### Prerequisites
- Python 3.8+
- pip package manager

#### Setup

```bash
# Clone the repository
git clone <repository-url>
cd example02

# Install dependencies
pip install -r requirements.txt

# Verify installation
python check_dependencies.py

# Run the application
streamlit run app.py
```

The application will open in your browser at: `http://localhost:8501`

#### 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t website-analyzer .

# Run container
docker run -p 8501:8501 website-analyzer
```

---

## 📖 How to Use

### 1. **📁 Data Loading**

#### Demo Data
Use the built-in sample dataset to explore all features immediately.

#### File Upload
Upload your own data files:
- **Supported formats:** Excel (.xlsx, .xls), CSV (.csv)
- **File validation:** Automatic format checking and error reporting
- **Date detection:** Smart identification of date columns

### 2. **📊 Analysis Dashboard**

#### KPI Metrics Panel
- Total sessions/sales count
- Average daily performance
- Growth rate calculations
- Peak performance indicators

#### Interactive Charts
- **Time Series:** Dynamic plots with zoom and pan capabilities
- **Product Comparison:** Bar charts, pie charts, donut charts
- **Correlation Analysis:** Heatmaps showing relationships between products
- **Seasonal Patterns:** Decomposition of time series data

### 3. **⚙️ Analysis Controls**

#### Date Range Filtering
- Custom date range selection
- Automatic date validation
- Period-based analysis

#### Visualization Options
- **Smoothing:** Moving averages with configurable window sizes
- **Anomaly Detection:** Z-score and IQR-based outlier identification
- **Chart Types:** Multiple visualization options for different insights

### 4. **📋 Data Export**

- **CSV Export:** Download processed data
- **Chart Export:** Save visualizations as images
- **Summary Reports:** Automated insights generation

---

## 📋 Data Format Requirements

### File Structure

Your data file should follow this structure:

```
Date        | Product_1 | Product_2 | Product_3
2020-01-01  | 100       | 80        | 150
2020-02-01  | 120       | 90        | 160
2020-03-01  | 110       | 95        | 140
```

### Requirements

- **First Column:** Date column with recognizable date formats
  - Supported: `YYYY-MM-DD`, `DD.MM.YYYY`, `MM/DD/YYYY`, etc.
  - Can be named: Date, Дата, date, дата, или любое похожее название
- **Other Columns:** Numeric data representing sales, sessions, or metrics
- **Headers:** Clear column names for products/metrics
- **Data Quality:** No missing values in date column

### Supported Date Formats

- ISO format: `2020-01-01`
- European: `01.01.2020`
- US format: `01/01/2020`
- Month names: `Jan 1, 2020`
- And many more...

---

## 🔧 Advanced Features

### 📊 Statistical Analysis

- **Descriptive Statistics:** Mean, median, standard deviation, quartiles
- **Correlation Analysis:** Pearson correlation matrices with significance testing
- **Seasonal Decomposition:** Trend, seasonal, and residual components
- **Growth Analysis:** Period-over-period growth calculations

### 🔍 Anomaly Detection

- **Z-Score Method:** Statistical outlier detection
- **IQR Method:** Interquartile range-based detection
- **Configurable Thresholds:** Adjustable sensitivity settings
- **Visual Highlighting:** Clear marking of anomalous data points

### 📈 Visualization Engine

- **Plotly Integration:** Interactive, publication-ready charts
- **Responsive Design:** Mobile and desktop optimized
- **Export Options:** PNG, SVG, PDF export capabilities
- **Theme Support:** Professional styling with consistent branding

### 🛡️ Data Validation

- **File Format Validation:** Comprehensive file type checking
- **Data Quality Checks:** Missing value detection and handling
- **Error Reporting:** Detailed validation feedback
- **Auto-correction:** Smart data type inference and conversion

---

## 🏗️ Technical Architecture

### 📚 Core Components

- **`app.py`** - Main Streamlit application with UI orchestration
- **`data_loader.py`** - Data ingestion and processing layer
- **`analysis.py`** - Statistical analysis engine
- **`plotting.py`** - Visualization layer using Plotly
- **`help_page.py`** - Comprehensive help system

### 🛠️ Technology Stack

- **Frontend:** Streamlit 1.49.1
- **Visualization:** Plotly 6.3.0, Interactive charts
- **Data Processing:** Pandas 2.3.2, NumPy 2.3.3
- **Statistics:** Statsmodels 0.14.5
- **File Support:** openpyxl 3.1.5 for Excel files
- **Testing:** pytest, pytest-cov for comprehensive testing
- **Code Quality:** flake8, black for code standards

### 🚀 CI/CD Pipeline

- **GitHub Actions:** Automated testing and deployment
- **Docker Hub:** Automated image building and publishing
- **Quality Gates:** Code style checking, test coverage
- **Multi-environment:** Support for development and production builds

### 🐳 Docker Configuration

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .
EXPOSE 8501

# Verify dependencies and create secure user
RUN python check_dependencies.py
RUN useradd --create-home --shell /bin/bash app
USER app

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🧪 Testing & Quality

### Test Suite

```bash
# Run all tests
python -m pytest -v

# Run with coverage
python -m pytest --cov=analysis --cov=data_loader --cov-report=term-missing

# Run specific test files
python -m pytest test_analysis.py -v
python -m pytest test_compatibility.py -v

# Custom functional tests
python test_refactored.py
```

### Code Quality

```bash
# Format code
python -m black *.py

# Check code style
python -m flake8 *.py --max-line-length=120 --ignore=E203,W503

# Verify dependencies
python check_dependencies.py
```

### Quality Standards

- **PEP 8 Compliance:** Enforced via flake8
- **Type Hints:** Comprehensive typing for all functions
- **Documentation:** Google-style docstrings
- **Test Coverage:** >90% coverage target
- **Modular Design:** Single responsibility principle

---

## 🔄 Development Workflow

### Local Development

1. **Setup Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Development Server:**
   ```bash
   streamlit run app.py
   ```

3. **Run Tests:**
   ```bash
   python -m pytest
   ```

### CI/CD Process

1. **Code Push** → GitHub repository
2. **Automated Testing** → pytest, flake8, dependency checks
3. **Docker Build** → Multi-stage build for optimization
4. **Deployment** → Docker Hub publication
5. **Production** → Streamlit Cloud deployment

---

## 📚 Documentation

### Complete Documentation
- **[CLAUDE.md](CLAUDE.md)** - Comprehensive development guide
- **[Docker Setup](Dockerfile)** - Container configuration
- **[CI/CD Pipeline](.github/workflows/ci-cd.yml)** - Automated workflows

### API Reference
- **Data Loading:** `data_loader.py` module documentation
- **Analysis Functions:** `analysis.py` statistical methods
- **Plotting Library:** `plotting.py` visualization functions

### Help System
- **Built-in Help:** Available in application sidebar
- **Interactive Examples:** Sample data and use cases
- **FAQ Section:** Common questions and solutions

---

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include comprehensive docstrings
- Write tests for new features
- Update documentation as needed

### Issue Reporting

Please use GitHub Issues for:
- Bug reports
- Feature requests
- Documentation improvements
- Performance issues

---

## 📈 Performance & Scalability

### Optimization Features

- **Data Caching:** Streamlit's `@st.cache_data` for performance
- **Memory Management:** Efficient pandas operations
- **Lazy Loading:** On-demand computation of statistics
- **Responsive UI:** Progressive disclosure of functionality

### Scalability Considerations

- **File Size Limits:** Optimized for files up to 100MB
- **Memory Usage:** Efficient data processing algorithms
- **Browser Performance:** Optimized chart rendering
- **Concurrent Users:** Stateless design for multiple users

---

## 🔒 Security & Privacy

### Data Security

- **No Data Storage:** Files processed in memory only
- **Local Processing:** No data transmitted to external services
- **File Validation:** Comprehensive input sanitization
- **Error Handling:** Secure error messages without data exposure

### Privacy Features

- **Session Isolation:** Each user session is independent
- **Temporary Processing:** Data cleared after session
- **No Logging:** No sensitive data logging
- **HTTPS Support:** Secure connections in production

---

## 🆘 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Verify installation
python check_dependencies.py
```

#### File Upload Issues
- **Format:** Ensure file is Excel (.xlsx, .xls) or CSV
- **Size:** Keep files under 100MB for optimal performance
- **Date Column:** First column should contain recognizable dates
- **Encoding:** Use UTF-8 encoding for CSV files

#### Performance Issues
- **File Size:** Reduce file size or sample data
- **Browser:** Try a different browser or clear cache
- **Memory:** Close other applications to free up memory

### Error Messages

| Error | Solution |
|-------|----------|
| "Date column not found" | Ensure first column contains dates |
| "Invalid file format" | Check file extension and content |
| "Memory error" | Reduce file size or restart application |
| "Import error" | Reinstall dependencies |

---

## 📞 Support

### Getting Help

1. **Built-in Help:** Use the "📚 Help" tab in the application
2. **Documentation:** Check `CLAUDE.md` for detailed information
3. **Demo Data:** Use sample data to test functionality
4. **GitHub Issues:** Report bugs or request features

### Contact Information

- **Repository:** GitHub repository link
- **Issues:** Use GitHub Issues for bug reports
- **Documentation:** See CLAUDE.md for comprehensive guide

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **[Russian Documentation](README-ru.md)** - Русская документация
- **[Live Demo](https://example02.streamlit.app/)** - Try the application
- **[Development Guide](CLAUDE.md)** - Comprehensive development documentation
- **[Docker Hub](https://hub.docker.com/)** - Container registry (configure with your Docker Hub username)

---

*Last updated: $(date +'%Y-%m-%d') | Built with ❤️ using Streamlit and Python*