"""
Модуль для создания интерактивных графиков.

Этот модуль содержит функции для создания различных типов
визуализаций с использованием Plotly для анализа данных о продажах.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def create_sales_timeline(
    df: pd.DataFrame,
    title: str = "Динамика продаж по времени",
    smoothing: bool = False,
    window: int = 7,
) -> go.Figure:
    """
    Создает интерактивный график временного ряда продаж.

    Args:
        df (pd.DataFrame): DataFrame с данными о продажах
        title (str): Заголовок графика
        smoothing (bool): Применять ли сглаживание
        window (int): Размер окна для скользящего среднего

    Returns:
        go.Figure: Объект графика Plotly
    """
    try:
        if df.empty:
            return go.Figure().add_annotation(
                text="Нет данных для отображения",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        fig = go.Figure()

        # Рассчитываем общие продажи по дням
        total_sales = df.sum(axis=1)

        # Основная линия
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=total_sales,
                mode="lines+markers",
                name="Общие продажи",
                line=dict(color="#1f77b4", width=2),
                marker=dict(size=4),
                hovertemplate="<b>Дата:</b> %{x}<br><b>Продажи:</b> %{y:,.0f}<extra></extra>",
            )
        )

        # Добавляем сглаженную линию если требуется
        if smoothing and len(total_sales) >= window:
            smoothed_sales = total_sales.rolling(window=window, center=True).mean()
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=smoothed_sales,
                    mode="lines",
                    name=f"Скользящее среднее ({window} дней)",
                    line=dict(color="#ff7f0e", width=3, dash="dash"),
                    hovertemplate="<b>Дата:</b> %{x}<br><b>Сглаженные продажи:</b> %{y:,.1f}<extra></extra>",
                )
            )

        # Настройка макета
        fig.update_layout(
            title={"text": title, "x": 0.5, "xanchor": "center", "font": {"size": 20}},
            xaxis_title="Дата",
            yaxis_title="Количество продаж",
            hovermode="x unified",
            showlegend=True,
            height=500,
            template="plotly_white",
        )

        return fig

    except Exception as e:
        st.error(f"Ошибка при создании графика временного ряда: {str(e)}")
        return go.Figure()


def create_product_comparison(df: pd.DataFrame, chart_type: str = "bar") -> go.Figure:
    """
    Создает график сравнения продуктов.

    Args:
        df (pd.DataFrame): DataFrame с данными о продажах
        chart_type (str): Тип графика ('bar', 'pie', 'donut')

    Returns:
        go.Figure: Объект графика Plotly
    """
    try:
        if df.empty:
            return go.Figure().add_annotation(
                text="Нет данных для отображения",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        # Рассчитываем общие продажи по продуктам
        product_totals = df.sum().sort_values(ascending=False)

        if chart_type == "bar":
            fig = px.bar(
                x=product_totals.index,
                y=product_totals.values,
                title="Сравнение общих продаж по продуктам",
                labels={"x": "Продукт", "y": "Общие продажи"},
                color=product_totals.values,
                color_continuous_scale="Blues",
            )

            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Общие продажи: %{y:,.0f}<extra></extra>"
            )

        elif chart_type in ["pie", "donut"]:
            fig = px.pie(
                values=product_totals.values,
                names=product_totals.index,
                title="Распределение продаж по продуктам",
            )

            if chart_type == "donut":
                fig.update_traces(hole=0.4)

            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>Продажи: %{value:,.0f}<br>Доля: %{percent}<extra></extra>"
            )

        fig.update_layout(
            title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
            height=400,
            template="plotly_white",
        )

        return fig

    except Exception as e:
        st.error(f"Ошибка при создании графика сравнения продуктов: {str(e)}")
        return go.Figure()


def create_heatmap(df: pd.DataFrame, metric: str = "sales") -> go.Figure:
    """
    Создает тепловую карту продаж.

    Args:
        df (pd.DataFrame): DataFrame с данными
        metric (str): Метрика для отображения

    Returns:
        go.Figure: Объект графика Plotly
    """
    try:
        if df.empty:
            return go.Figure().add_annotation(
                text="Нет данных для отображения",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        # Создаем сводную таблицу по месяцам и продуктам
        df_copy = df.copy()
        df_copy["Месяц"] = df_copy.index.strftime("%Y-%m")
        df_copy["День_недели"] = df_copy.index.day_name()

        # Группировка по месяцам
        monthly_data = df_copy.groupby("Месяц")[df.columns].sum()

        fig = go.Figure(
            data=go.Heatmap(
                z=monthly_data.values,
                x=monthly_data.columns,
                y=monthly_data.index,
                colorscale="Blues",
                hoverongaps=False,
                hovertemplate="<b>Месяц:</b> %{y}<br><b>Продукт:</b> %{x}<br><b>Продажи:</b> %{z:,.0f}<extra></extra>",
            )
        )

        fig.update_layout(
            title={
                "text": "Тепловая карта продаж по месяцам и продуктам",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18},
            },
            xaxis_title="Продукты",
            yaxis_title="Месяцы",
            height=500,
            template="plotly_white",
        )

        return fig

    except Exception as e:
        st.error(f"Ошибка при создании тепловой карты: {str(e)}")
        return go.Figure()


def create_correlation_matrix(correlation_df: pd.DataFrame) -> go.Figure:
    """
    Создает тепловую карту корреляции между продуктами.

    Args:
        correlation_df (pd.DataFrame): Корреляционная матрица

    Returns:
        go.Figure: Объект графика Plotly
    """
    try:
        if correlation_df.empty:
            return go.Figure().add_annotation(
                text="Нет данных для отображения",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        fig = go.Figure(
            data=go.Heatmap(
                z=correlation_df.values,
                x=correlation_df.columns,
                y=correlation_df.index,
                colorscale="RdBu",
                zmid=0,
                zmin=-1,
                zmax=1,
                hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>Корреляция: %{z:.3f}<extra></extra>",
            )
        )

        fig.update_layout(
            title={
                "text": "Корреляционная матрица между продуктами",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18},
            },
            height=400,
            template="plotly_white",
        )

        return fig

    except Exception as e:
        st.error(f"Ошибка при создании корреляционной матрицы: {str(e)}")
        return go.Figure()


def create_seasonal_plot(df: pd.DataFrame, column: str) -> go.Figure:
    """
    Создает график сезонных паттернов.

    Args:
        df (pd.DataFrame): DataFrame с данными
        column (str): Столбец для анализа

    Returns:
        go.Figure: Объект графика Plotly
    """
    try:
        if df.empty or column not in df.columns:
            return go.Figure().add_annotation(
                text="Нет данных для отображения",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        # Создаем DataFrame с месячными данными
        df_copy = df.copy()
        df_copy["Месяц"] = df_copy.index.month
        df_copy["Год"] = df_copy.index.year

        # Группируем по месяцам
        monthly_avg = df_copy.groupby("Месяц")[column].mean()

        month_names = [
            "Янв",
            "Фев",
            "Мар",
            "Апр",
            "Май",
            "Июн",
            "Июл",
            "Авг",
            "Сен",
            "Окт",
            "Ноя",
            "Дек",
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=[month_names[i - 1] for i in monthly_avg.index],
                y=monthly_avg.values,
                mode="lines+markers",
                name=f"Средние продажи {column}",
                line=dict(color="#2E86AB", width=3),
                marker=dict(size=8),
                hovertemplate="<b>Месяц:</b> %{x}<br><b>Средние продажи:</b> %{y:,.1f}<extra></extra>",
            )
        )

        fig.update_layout(
            title={
                "text": f"Сезонные паттерны продаж - {column}",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18},
            },
            xaxis_title="Месяц",
            yaxis_title="Средние продажи",
            height=400,
            template="plotly_white",
        )

        return fig

    except Exception as e:
        st.error(f"Ошибка при создании сезонного графика: {str(e)}")
        return go.Figure()


def create_growth_chart(df: pd.DataFrame) -> go.Figure:
    """
    Создает график роста продаж по периодам.

    Args:
        df (pd.DataFrame): DataFrame с данными

    Returns:
        go.Figure: Объект графика Plotly
    """
    try:
        if df.empty:
            return go.Figure().add_annotation(
                text="Нет данных для отображения",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        # Рассчитываем месячные суммы
        monthly_data = df.resample("M").sum()
        total_monthly = monthly_data.sum(axis=1)

        # Рассчитываем процентный рост
        growth_rate = total_monthly.pct_change() * 100

        fig = go.Figure()

        # График роста
        colors = ["red" if x < 0 else "green" for x in growth_rate.values]

        fig.add_trace(
            go.Bar(
                x=monthly_data.index,
                y=growth_rate.values,
                marker_color=colors,
                name="Темп роста (%)",
                hovertemplate="<b>Месяц:</b> %{x}<br><b>Рост:</b> %{y:.1f}%<extra></extra>",
            )
        )

        # Добавляем нулевую линию
        fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)

        fig.update_layout(
            title={
                "text": "Месячный темп роста продаж",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18},
            },
            xaxis_title="Месяц",
            yaxis_title="Темп роста (%)",
            height=400,
            template="plotly_white",
            showlegend=False,
        )

        return fig

    except Exception as e:
        st.error(f"Ошибка при создании графика роста: {str(e)}")
        return go.Figure()


def create_distribution_plot(df: pd.DataFrame, column: str) -> go.Figure:
    """
    Создает график распределения для указанного столбца.

    Args:
        df (pd.DataFrame): DataFrame с данными
        column (str): Столбец для анализа

    Returns:
        go.Figure: Объект графика Plotly
    """
    try:
        if df.empty or column not in df.columns:
            return go.Figure().add_annotation(
                text="Нет данных для отображения",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        fig = px.histogram(
            df,
            x=column,
            nbins=30,
            title=f"Распределение значений - {column}",
            labels={"x": column, "y": "Частота"},
        )

        fig.update_layout(
            title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
            height=400,
            template="plotly_white",
        )

        return fig

    except Exception as e:
        st.error(f"Ошибка при создании графика распределения: {str(e)}")
        return go.Figure()
