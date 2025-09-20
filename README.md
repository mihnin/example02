# 📊 Анализатор Трафика Веб-сайта | Website Traffic Analyzer

**🌐 Демо:** https://example02.streamlit.app/

Интерактивное веб-приложение для анализа и визуализации данных о продажах/трафике с использованием Streamlit, Plotly и продвинутой аналитики.

Interactive web application for sales/traffic data analysis and visualization using Streamlit, Plotly, and advanced analytics.

---

## 🎯 Предназначение | Purpose

### 🇷🇺 Русский
**Анализатор Трафика Веб-сайта** — это мощный инструмент для бизнес-аналитики, предназначенный для:

- **📈 Анализа продаж и трафика** - загрузка и обработка данных временных рядов
- **📊 Визуализации данных** - интерактивные графики, тепловые карты, корреляционный анализ
- **🎯 KPI мониторинга** - автоматический расчет ключевых показателей эффективности
- **🔍 Обнаружения аномалий** - выявление необычных паттернов в данных
- **📋 Генерации инсайтов** - автоматические выводы и рекомендации

**Бизнес-смысл:**
- Принятие решений на основе данных
- Мониторинг эффективности продаж/маркетинга
- Выявление сезонных трендов и паттернов
- Прогнозирование и планирование

### 🇺🇸 English
**Website Traffic Analyzer** is a powerful business intelligence tool designed for:

- **📈 Sales & Traffic Analysis** - loading and processing time series data
- **📊 Data Visualization** - interactive charts, heatmaps, correlation analysis
- **🎯 KPI Monitoring** - automatic calculation of key performance indicators
- **🔍 Anomaly Detection** - identifying unusual patterns in data
- **📋 Insight Generation** - automated conclusions and recommendations

**Business Value:**
- Data-driven decision making
- Sales/marketing performance monitoring
- Seasonal trends and pattern identification
- Forecasting and planning

---

## 🚀 Быстрый старт | Quick Start

### 🌐 Онлайн-использование | Online Usage

Просто перейдите по ссылке: **https://example02.streamlit.app/**

Just visit: **https://example02.streamlit.app/**

### 💻 Локальный запуск | Local Setup

#### Требования | Requirements
- Python 3.8+
- pip

#### Установка | Installation

```bash
# Клонирование репозитория | Clone repository
git clone <repository-url>
cd example02

# Установка зависимостей | Install dependencies
pip install -r requirements.txt

# Проверка зависимостей | Check dependencies
python check_dependencies.py

# Запуск приложения | Run application
streamlit run app.py
```

Приложение откроется в браузере по адресу: `http://localhost:8501`

Application will open in browser at: `http://localhost:8501`

---

## 📖 Как пользоваться | How to Use

### 🔧 Основной интерфейс | Main Interface

#### 1. **📁 Загрузка данных | Data Loading**
- **🎯 Демо данные:** Используйте встроенный пример для знакомства
- **⬆️ Загрузка файла:** Загрузите Excel (.xlsx, .xls) или CSV файл
- **Demo data:** Use built-in sample to explore features
- **File upload:** Upload Excel (.xlsx, .xls) or CSV file

#### 2. **📊 Панель анализа | Analysis Dashboard**
- **KPI Метрики:** Общие показатели (сессии, рост, средние значения)
- **Интерактивные графики:** Временные ряды с возможностью сглаживания
- **Сравнение продуктов:** Столбчатые, круговые диаграммы
- **KPI Metrics:** Overall indicators (sessions, growth, averages)
- **Interactive Charts:** Time series with smoothing options
- **Product Comparison:** Bar charts, pie charts

#### 3. **⚙️ Настройки | Settings**
В боковой панели доступны:
- **📅 Диапазон дат:** Фильтрация по периодам
- **📈 Сглаживание:** Скользящее среднее
- **🔍 Обнаружение аномалий:** Выделение необычных значений

Sidebar controls:
- **📅 Date Range:** Filter by time periods
- **📈 Smoothing:** Moving averages
- **🔍 Anomaly Detection:** Highlight unusual values

### 📋 Формат данных | Data Format

#### Требования к файлу | File Requirements:
- **Первый столбец:** Даты (YYYY-MM-DD, DD.MM.YYYY, etc.)
- **Остальные столбцы:** Числовые данные (продажи, сессии, etc.)
- **First column:** Dates (YYYY-MM-DD, DD.MM.YYYY, etc.)
- **Other columns:** Numeric data (sales, sessions, etc.)

#### Пример | Example:
```
Дата        | Продукт_1 | Продукт_2 | Продукт_3
2020-01-01  | 100       | 80        | 150
2020-02-01  | 120       | 90        | 160
2020-03-01  | 110       | 95        | 140
```

---

## 🔧 Возможности | Features

### 📊 Аналитика | Analytics
- **Описательная статистика** | Descriptive statistics
- **Корреляционный анализ** | Correlation analysis
- **Сезонная декомпозиция** | Seasonal decomposition
- **Обнаружение аномалий** | Anomaly detection
- **Автоматические инсайты** | Automated insights

### 📈 Визуализация | Visualization
- **Временные ряды** | Time series plots
- **Тепловые карты** | Heatmaps
- **Графики роста** | Growth charts
- **Распределения** | Distribution plots
- **Интерактивность** | Interactive features

### 💾 Экспорт | Export
- **CSV данные** | CSV data export
- **PNG графики** | PNG chart export
- **PDF отчеты** | PDF reports

---

## 🏢 Применение в бизнесе | Business Applications

### E-commerce
- Анализ продаж по продуктам | Product sales analysis
- Мониторинг конверсии | Conversion monitoring
- Сезонные тренды | Seasonal trends

### Веб-аналитика | Web Analytics
- Трафик по каналам | Traffic by channels
- Поведение пользователей | User behavior
- A/B тестирование | A/B testing

### Маркетинг | Marketing
- ROI кампаний | Campaign ROI
- Эффективность каналов | Channel performance
- Прогнозирование | Forecasting

---

## 🛠️ Технические детали | Technical Details

### Стек технологий | Tech Stack
- **Frontend:** Streamlit
- **Visualization:** Plotly, Matplotlib
- **Analytics:** Pandas, NumPy, Statsmodels
- **Data:** Excel, CSV support

### Архитектура | Architecture
- **Модульная структура** | Modular structure
- **Кэширование данных** | Data caching
- **Валидация файлов** | File validation
- **Обработка ошибок** | Error handling

---

## 📚 Документация | Documentation

- **📖 Полная документация:** `CLAUDE.md`
- **🧪 Тесты:** `test_analysis.py`, `test_compatibility.py`
- **🔍 Проверка зависимостей:** `check_dependencies.py`

---

## 📞 Поддержка | Support

При возникновении вопросов:
1. Изучите встроенную справку (вкладка "📚 Справка")
2. Проверьте формат ваших данных
3. Используйте демо данные для тестирования

For questions:
1. Check built-in help (tab "📚 Help")
2. Verify your data format
3. Use demo data for testing

---

## 📄 Лицензия | License

MIT License - см. файл `LICENSE` | see `LICENSE` file
