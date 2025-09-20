"""
Модуль для анализа данных.

Этот модуль содержит функции для выполнения различных видов
статистического анализа данных о продажах.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime, date


def calculate_basic_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Рассчитывает базовую статистику для каждого продукта.

    Args:
        df (pd.DataFrame): DataFrame с данными о продажах

    Returns:
        Dict[str, Dict[str, float]]: Словарь со статистикой по каждому продукту
    """
    try:
        if df.empty:
            return {}

        statistics = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns

        for column in numeric_columns:
            statistics[column] = {
                "mean": float(df[column].mean()),
                "median": float(df[column].median()),
                "std": float(df[column].std()),
                "min": float(df[column].min()),
                "max": float(df[column].max()),
                "sum": float(df[column].sum()),
                "count": int(df[column].count()),
            }

        return statistics

    except Exception as e:
        st.error(f"Ошибка при расчете базовой статистики: {str(e)}")
        return {}


def calculate_kpi_metrics(df: pd.DataFrame) -> Dict[str, Union[int, float]]:
    """
    Рассчитывает ключевые показатели эффективности (KPI).

    Args:
        df (pd.DataFrame): DataFrame с данными о продажах

    Returns:
        Dict[str, Union[int, float]]: Словарь с KPI метриками
    """
    try:
        if df.empty:
            return {
                "total_sessions": 0,
                "avg_daily_sessions": 0.0,
                "max_daily_sessions": 0,
            }

        # Рассчитываем общее количество продаж (сумма по всем продуктам)
        total_sales = df.sum(axis=1)

        kpi_metrics = {
            "total_sessions": int(total_sales.sum()),
            "avg_daily_sessions": float(total_sales.mean()),
            "max_daily_sessions": int(total_sales.max()),
            "min_daily_sessions": int(total_sales.min()),
            "days_count": len(df),
            "growth_rate": _calculate_growth_rate(total_sales),
        }

        return kpi_metrics

    except Exception as e:
        st.error(f"Ошибка при расчете KPI метрик: {str(e)}")
        return {}


def _calculate_growth_rate(series: pd.Series) -> float:
    """
    Рассчитывает темп роста между первым и последним значением.

    Args:
        series (pd.Series): Временной ряд данных

    Returns:
        float: Темп роста в процентах
    """
    try:
        if len(series) < 2:
            return 0.0

        first_value = series.iloc[0]
        last_value = series.iloc[-1]

        if first_value == 0:
            return 0.0

        growth_rate = ((last_value - first_value) / first_value) * 100
        return float(growth_rate)

    except Exception:
        return 0.0


def calculate_moving_average(
    df: pd.DataFrame, window: int = 7, column: Optional[str] = None
) -> pd.DataFrame:
    """
    Рассчитывает скользящее среднее для указанного столбца или всех столбцов.

    Args:
        df (pd.DataFrame): Исходный DataFrame
        window (int): Размер окна для скользящего среднего
        column (Optional[str]): Название столбца (если None, применяется ко всем)

    Returns:
        pd.DataFrame: DataFrame со скользящими средними
    """
    try:
        if df.empty:
            return pd.DataFrame()

        if column and column in df.columns:
            result = df.copy()
            result[f"{column}_MA{window}"] = df[column].rolling(window=window).mean()
            return result
        else:
            # Применяем ко всем числовым столбцам
            result = df.copy()
            numeric_columns = df.select_dtypes(include=[np.number]).columns

            for col in numeric_columns:
                result[f"{col}_MA{window}"] = df[col].rolling(window=window).mean()

            return result

    except Exception as e:
        st.error(f"Ошибка при расчете скользящего среднего: {str(e)}")
        return df


def detect_anomalies(
    df: pd.DataFrame, threshold: float = 2.0, method: str = "zscore"
) -> Dict[str, List[Tuple[datetime, float]]]:
    """
    Обнаруживает аномалии в данных.

    Args:
        df (pd.DataFrame): DataFrame с данными
        threshold (float): Пороговое значение для определения аномалий
        method (str): Метод обнаружения ('zscore' или 'iqr')

    Returns:
        Dict[str, List[Tuple[datetime, float]]]: Словарь с аномалиями по столбцам
    """
    try:
        if df.empty:
            return {}

        anomalies = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns

        for column in numeric_columns:
            column_anomalies = []

            if method == "zscore":
                z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                anomaly_mask = z_scores > threshold

            elif method == "iqr":
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                anomaly_mask = (df[column] < lower_bound) | (df[column] > upper_bound)

            else:
                continue

            anomaly_dates = df[anomaly_mask].index
            anomaly_values = df.loc[anomaly_mask, column]

            for date, value in zip(anomaly_dates, anomaly_values):
                column_anomalies.append((date, float(value)))

            anomalies[column] = column_anomalies

        return anomalies

    except Exception as e:
        st.error(f"Ошибка при обнаружении аномалий: {str(e)}")
        return {}


def calculate_seasonal_decomposition(
    df: pd.DataFrame, column: str, period: int = 12
) -> Optional[Dict[str, pd.Series]]:
    """
    Выполняет сезонную декомпозицию временного ряда.

    Args:
        df (pd.DataFrame): DataFrame с данными
        column (str): Название столбца для анализа
        period (int): Период сезонности

    Returns:
        Optional[Dict[str, pd.Series]]: Компоненты декомпозиции или None
    """
    try:
        if df.empty or column not in df.columns:
            return None

        from statsmodels.tsa.seasonal import seasonal_decompose

        # Убираем пропущенные значения
        series = df[column].dropna()

        if len(series) < 2 * period:
            st.warning(
                f"Недостаточно данных для сезонной декомпозиции столбца {column}"
            )
            return None

        decomposition = seasonal_decompose(series, model="additive", period=period)

        return {
            "trend": decomposition.trend,
            "seasonal": decomposition.seasonal,
            "residual": decomposition.resid,
            "observed": decomposition.observed,
        }

    except Exception as e:
        st.warning(f"Не удалось выполнить сезонную декомпозицию: {str(e)}")
        return None


def calculate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Рассчитывает корреляционную матрицу между продуктами.

    Args:
        df (pd.DataFrame): DataFrame с данными о продажах

    Returns:
        pd.DataFrame: Корреляционная матрица
    """
    try:
        if df.empty:
            return pd.DataFrame()

        numeric_columns = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_columns].corr()

        return correlation_matrix

    except Exception as e:
        st.error(f"Ошибка при расчете корреляционной матрицы: {str(e)}")
        return pd.DataFrame()


def generate_insights(df: pd.DataFrame, statistics: Dict) -> List[str]:
    """
    Генерирует автоматические инсайты на основе анализа данных.

    Args:
        df (pd.DataFrame): DataFrame с данными
        statistics (Dict): Статистические данные

    Returns:
        List[str]: Список инсайтов
    """
    try:
        if df.empty or not statistics:
            return ["Недостаточно данных для генерации инсайтов"]

        insights = []

        # Анализ роста
        total_sales = df.sum(axis=1)
        if len(total_sales) >= 2:
            growth_rate = _calculate_growth_rate(total_sales)
            if growth_rate > 10:
                insights.append(
                    f"Положительная динамика: рост продаж составил {growth_rate:.1f}%"
                )
            elif growth_rate < -10:
                insights.append(
                    f"Отрицательная динамика: снижение продаж на {abs(growth_rate):.1f}%"
                )

        # Анализ лучшего продукта
        if statistics:
            product_totals = {
                product: stats["sum"] for product, stats in statistics.items()
            }
            best_product = max(product_totals, key=product_totals.get)
            insights.append(
                f"Лидер продаж: {best_product} с общим объемом {product_totals[best_product]:,.0f}"
            )

        # Анализ волатильности
        for product, stats in statistics.items():
            cv = stats["std"] / stats["mean"] if stats["mean"] > 0 else 0
            if cv > 0.5:
                insights.append(
                    f"{product}: высокая волатильность продаж (CV = {cv:.2f})"
                )

        # Анализ сезонности
        if len(df) >= 12:
            monthly_avg = df.groupby(df.index.month).mean().sum(axis=1)
            peak_month = monthly_avg.idxmax()
            month_names = [
                "",
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь",
            ]
            insights.append(f"Пиковый месяц продаж: {month_names[peak_month]}")

        return insights

    except Exception as e:
        st.error(f"Ошибка при генерации инсайтов: {str(e)}")
        return ["Ошибка при анализе данных"]
