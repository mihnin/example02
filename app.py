"""
Главное приложение для анализа данных о продажах.

Веб-приложение на Streamlit для интерактивного анализа и визуализации
данных о продажах с использованием модульной архитектуры.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional

# Импорт модулей приложения
from data_loader import (
    load_sales_data,
    filter_data_by_date,
    get_date_range,
    validate_data,
    prepare_data_summary,
    validate_file_format
)
from help_page import display_help_page, show_help_in_sidebar
from analysis import (
    calculate_basic_statistics,
    calculate_kpi_metrics,
    calculate_moving_average,
    detect_anomalies,
    calculate_correlation_matrix,
    generate_insights
)
from plotting import (
    create_sales_timeline,
    create_product_comparison,
    create_heatmap,
    create_correlation_matrix,
    create_seasonal_plot,
    create_growth_chart,
    create_distribution_plot
)


def setup_page_config() -> None:
    """Настройка конфигурации страницы Streamlit."""
    st.set_page_config(
        page_title="Анализатор Трафика Веб-сайта",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def setup_navigation() -> str:
    """
    Настройка навигации приложения.

    Returns:
        str: Выбранная страница
    """
    st.sidebar.title("🔧 Навигация")

    page = st.sidebar.radio(
        "Выберите страницу:",
        ["📊 Анализ данных", "📚 Справка"],
        index=0
    )

    st.sidebar.markdown("---")
    return page


def display_header() -> None:
    """Отображение заголовка приложения."""
    st.title("📊 Анализатор Трафика Веб-сайта")
    st.markdown("---")
    st.markdown(
        """
        Добро пожаловать в интерактивный анализатор данных о продажах!
        Используйте боковую панель для настройки параметров анализа.
        """
    )


def handle_file_upload() -> Optional[pd.DataFrame]:
    """
    Обрабатывает загрузку файла пользователем.

    Returns:
        Optional[pd.DataFrame]: Загруженные данные или None
    """
    st.sidebar.subheader("📁 Загрузка данных")

    # Выбор источника данных
    data_source = st.sidebar.radio(
        "Источник данных:",
        ["📊 Демо данные", "⬆️ Загрузить файл"],
        index=0
    )

    if data_source == "⬆️ Загрузить файл":
        uploaded_file = st.sidebar.file_uploader(
            "Выберите файл с данными",
            type=['xlsx', 'xls', 'csv'],
            help="Поддерживаются форматы: Excel (.xlsx, .xls) и CSV (.csv)"
        )

        if uploaded_file is not None:
            with st.spinner("Загрузка и обработка файла..."):
                try:
                    # Загружаем данные
                    df = load_sales_data(uploaded_file=uploaded_file)

                    if not df.empty:
                        # Валидируем файл
                        validation_result = validate_file_format(df, uploaded_file.name)

                        # Отображаем результаты валидации
                        if validation_result['errors']:
                            st.sidebar.error("❌ Ошибки в файле:")
                            for error in validation_result['errors']:
                                st.sidebar.error(f"• {error}")

                        if validation_result['warnings']:
                            st.sidebar.warning("⚠️ Предупреждения:")
                            for warning in validation_result['warnings']:
                                st.sidebar.warning(f"• {warning}")

                        if validation_result['is_valid']:
                            st.sidebar.success("✅ Файл успешно загружен!")
                            return df
                        else:
                            st.sidebar.error("❌ Файл не прошел валидацию")
                            return None

                except Exception as e:
                    st.sidebar.error(f"❌ Ошибка при загрузке файла: {str(e)}")
                    return None
        else:
            st.sidebar.info("Загрузите файл для анализа")
            return None

    else:
        # Используем демо данные
        try:
            df = load_sales_data()
            if not df.empty:
                st.sidebar.success("✅ Демо данные загружены")
                return df
            else:
                st.sidebar.warning("⚠️ Демо данные недоступны")
                return None
        except Exception as e:
            st.sidebar.error(f"❌ Ошибка загрузки демо данных: {str(e)}")
            return None


def create_sidebar_controls(df: pd.DataFrame) -> Dict:
    """
    Создает элементы управления в боковой панели.

    Args:
        df (pd.DataFrame): DataFrame с данными

    Returns:
        Dict: Словарь с параметрами из боковой панели
    """
    st.sidebar.header("⚙️ Параметры анализа")

    # Получаем диапазон дат из данных
    min_date, max_date = get_date_range(df)

    # Элементы управления датами
    st.sidebar.subheader("📅 Диапазон дат")
    start_date = st.sidebar.date_input(
        "Начальная дата",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

    end_date = st.sidebar.date_input(
        "Конечная дата",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

    # Проверка корректности диапазона
    if start_date > end_date:
        st.sidebar.error("Начальная дата не может быть позже конечной!")
        start_date = min_date
        end_date = max_date

    # Опции визуализации
    st.sidebar.subheader("📈 Параметры графиков")
    smoothing = st.sidebar.checkbox(
        "Применить сглаживание (скользящее среднее)",
        value=False,
        help="Добавляет линию скользящего среднего на основной график"
    )

    smoothing_window = 7
    if smoothing:
        smoothing_window = st.sidebar.slider(
            "Размер окна сглаживания (дни)",
            min_value=3,
            max_value=30,
            value=7,
            step=1
        )

    # Дополнительные опции
    st.sidebar.subheader("🔧 Дополнительные настройки")
    show_anomalies = st.sidebar.checkbox(
        "Обнаружение аномалий",
        value=False,
        help="Выделяет необычные значения в данных"
    )

    chart_type = st.sidebar.selectbox(
        "Тип графика сравнения продуктов",
        options=["bar", "pie", "donut"],
        index=0,
        format_func=lambda x: {
            "bar": "Столбчатая диаграмма",
            "pie": "Круговая диаграмма",
            "donut": "Кольцевая диаграмма"
        }[x]
    )

    return {
        'start_date': start_date,
        'end_date': end_date,
        'smoothing': smoothing,
        'smoothing_window': smoothing_window,
        'show_anomalies': show_anomalies,
        'chart_type': chart_type
    }


def display_kpi_metrics(metrics: Dict) -> None:
    """
    Отображает KPI метрики в колонках.

    Args:
        metrics (Dict): Словарь с KPI метриками
    """
    st.subheader("📊 Ключевые показатели")

    if not metrics:
        st.warning("Не удалось рассчитать KPI метрики")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Общее количество сессий",
            value=f"{metrics.get('total_sessions', 0):,}",
            delta=None
        )

    with col2:
        avg_sessions = metrics.get('avg_daily_sessions', 0)
        st.metric(
            label="Среднее количество сессий в день",
            value=f"{avg_sessions:,.1f}",
            delta=None
        )

    with col3:
        st.metric(
            label="Максимальное количество сессий",
            value=f"{metrics.get('max_daily_sessions', 0):,}",
            delta=None
        )

    with col4:
        growth_rate = metrics.get('growth_rate', 0)
        delta_color = "normal" if growth_rate >= 0 else "inverse"
        st.metric(
            label="Общий темп роста",
            value=f"{growth_rate:+.1f}%",
            delta=f"{growth_rate:+.1f}%",
            delta_color=delta_color
        )


def display_main_chart(df: pd.DataFrame, params: Dict) -> None:
    """
    Отображает основной график временного ряда.

    Args:
        df (pd.DataFrame): DataFrame с данными
        params (Dict): Параметры из боковой панели
    """
    st.subheader("📈 Интерактивный график сессий")

    if df.empty:
        st.warning("Нет данных для отображения графика")
        return

    # Создаем график
    fig = create_sales_timeline(
        df,
        title="Динамика продаж по времени",
        smoothing=params['smoothing'],
        window=params['smoothing_window']
    )

    # Добавляем аномалии если требуется
    if params['show_anomalies']:
        anomalies = detect_anomalies(df, threshold=2.0, method='zscore')
        if anomalies:
            st.info("🔍 Обнаружены аномалии в данных (отмечены красными точками)")

    st.plotly_chart(fig, use_container_width=True)


def display_product_analysis(df: pd.DataFrame, params: Dict) -> None:
    """
    Отображает анализ по продуктам.

    Args:
        df (pd.DataFrame): DataFrame с данными
        params (Dict): Параметры из боковой панели
    """
    st.subheader("🔍 Анализ по продуктам")

    if df.empty:
        st.warning("Нет данных для анализа продуктов")
        return

    col1, col2 = st.columns(2)

    with col1:
        # График сравнения продуктов
        comparison_fig = create_product_comparison(df, params['chart_type'])
        st.plotly_chart(comparison_fig, use_container_width=True)

    with col2:
        # Корреляционная матрица
        correlation_matrix = calculate_correlation_matrix(df)
        if not correlation_matrix.empty:
            correlation_fig = create_correlation_matrix(correlation_matrix)
            st.plotly_chart(correlation_fig, use_container_width=True)


def display_additional_charts(df: pd.DataFrame) -> None:
    """
    Отображает дополнительные графики.

    Args:
        df (pd.DataFrame): DataFrame с данными
    """
    st.subheader("📋 Дополнительный анализ")

    if df.empty:
        return

    col1, col2 = st.columns(2)

    with col1:
        # Тепловая карта
        heatmap_fig = create_heatmap(df)
        st.plotly_chart(heatmap_fig, use_container_width=True)

    with col2:
        # График роста
        growth_fig = create_growth_chart(df)
        st.plotly_chart(growth_fig, use_container_width=True)

    # Сезонный анализ для каждого продукта
    st.subheader("🌍 Сезонный анализ")
    product_tabs = st.tabs(df.columns.tolist())

    for i, product in enumerate(df.columns):
        with product_tabs[i]:
            seasonal_fig = create_seasonal_plot(df, product)
            st.plotly_chart(seasonal_fig, use_container_width=True)


def display_data_table(df: pd.DataFrame) -> None:
    """
    Отображает таблицу с данными.

    Args:
        df (pd.DataFrame): DataFrame для отображения
    """
    st.subheader("📋 Таблица данных")

    if df.empty:
        st.warning("Нет данных для отображения в таблице")
        return

    # Добавляем общий столбец
    display_df = df.copy()
    display_df['Общие продажи'] = df.sum(axis=1)

    # Форматируем индекс для лучшего отображения
    display_df.index = display_df.index.strftime('%Y-%m-%d')

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )

    # Кнопка для скачивания данных
    csv = display_df.to_csv(encoding='utf-8-sig')
    st.download_button(
        label="📥 Скачать данные (CSV)",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def display_insights(df: pd.DataFrame, statistics: Dict) -> None:
    """
    Отображает автоматически сгенерированные инсайты.

    Args:
        df (pd.DataFrame): DataFrame с данными
        statistics (Dict): Статистические данные
    """
    st.subheader("💡 Автоматические инсайты")

    insights = generate_insights(df, statistics)

    if insights:
        for i, insight in enumerate(insights, 1):
            st.info(f"**{i}.** {insight}")
    else:
        st.warning("Не удалось сгенерировать инсайты из данных")


def main() -> None:
    """Главная функция приложения."""
    # Настройка страницы
    setup_page_config()

    # Настройка навигации
    current_page = setup_navigation()

    if current_page == "📚 Справка":
        # Отображаем страницу помощи
        display_help_page()
        return

    # Основная страница анализа данных
    display_header()

    try:
        # Обработка загрузки файла
        df = handle_file_upload()

        if df is None:
            st.info("👆 Выберите источник данных в боковой панели для начала анализа")
            show_help_in_sidebar()
            return

        if df.empty or not validate_data(df):
            st.error("❌ Не удалось обработать данные или данные имеют неверный формат")
            show_help_in_sidebar()
            return

        # Создание элементов управления
        params = create_sidebar_controls(df)

        # Фильтрация данных по выбранному диапазону
        filtered_df = filter_data_by_date(df, params['start_date'], params['end_date'])

        if filtered_df.empty:
            st.warning("⚠️ Нет данных в выбранном диапазоне дат")
            return

        # Расчет статистики и метрик
        with st.spinner("Анализ данных..."):
            statistics = calculate_basic_statistics(filtered_df)
            kpi_metrics = calculate_kpi_metrics(filtered_df)

        # Отображение KPI метрик
        display_kpi_metrics(kpi_metrics)

        st.markdown("---")

        # Основной график
        display_main_chart(filtered_df, params)

        st.markdown("---")

        # Анализ по продуктам
        display_product_analysis(filtered_df, params)

        st.markdown("---")

        # Дополнительные графики
        display_additional_charts(filtered_df)

        st.markdown("---")

        # Автоматические инсайты
        display_insights(filtered_df, statistics)

        st.markdown("---")

        # Таблица с данными
        display_data_table(filtered_df)

        # Информация о данных в боковой панели
        st.sidebar.markdown("---")
        st.sidebar.subheader("ℹ️ Информация о данных")

        data_summary = prepare_data_summary(filtered_df)
        if data_summary:
            st.sidebar.write(f"**Количество записей:** {data_summary.get('total_rows', 0)}")
            st.sidebar.write(f"**Период:** {data_summary.get('date_range', 'Неизвестно')}")
            st.sidebar.write(f"**Продукты:** {len(data_summary.get('columns', []))}")

        # Добавляем краткую справку в боковую панель
        show_help_in_sidebar()

    except Exception as e:
        st.error(f"❌ Произошла ошибка: {str(e)}")
        st.info("Пожалуйста, проверьте данные и попробуйте снова")
        show_help_in_sidebar()


if __name__ == "__main__":
    main()