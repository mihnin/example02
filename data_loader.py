"""
Модуль для загрузки и кэширования данных.

Этот модуль содержит функции для загрузки данных из Excel файлов
и подготовки их для анализа в Streamlit приложении.
"""

import pandas as pd
import streamlit as st
from datetime import datetime, date
from typing import Optional, Union, Dict, List
import os


@st.cache_data
def load_sales_data(file_path: Optional[str] = None, uploaded_file=None) -> pd.DataFrame:
    """
    Загружает данные о продажах из Excel файла с кэшированием.

    Args:
        file_path (Optional[str]): Путь к файлу с данными
        uploaded_file: Загруженный файл из Streamlit

    Returns:
        pd.DataFrame: DataFrame с данными о продажах

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если данные имеют неверный формат
    """
    try:
        # Определяем источник данных
        if uploaded_file is not None:
            # Загружаем из загруженного файла
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                raise ValueError("Поддерживаются только файлы .xlsx, .xls и .csv")
        elif file_path is not None:
            # Загружаем из локального файла
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {file_path} не найден")
            df = pd.read_excel(file_path)
        else:
            # Пытаемся загрузить дефолтный файл
            default_path = "docs/sample_sales_data.xlsx"
            if os.path.exists(default_path):
                df = pd.read_excel(default_path)
            else:
                raise FileNotFoundError("Файл данных не найден. Пожалуйста, загрузите файл.")

        # Определяем столбец с датами и переименовываем его
        date_column = None
        first_col = df.columns[0] if len(df.columns) > 0 else None

        # Ищем столбец с датами
        for col in df.columns:
            col_lower = str(col).lower()
            if ('дата' in col_lower or 'date' in col_lower or 'время' in col_lower or
                col == 'Unnamed: 0'):
                date_column = col
                break

        # Если не нашли явный столбец с датами, используем первый столбец
        if date_column is None and first_col is not None:
            try:
                # Проверяем, можно ли преобразовать первый столбец в даты
                pd.to_datetime(df[first_col].head())
                date_column = first_col
            except:
                raise ValueError("Первый столбец не содержит распознаваемые даты")

        if date_column is None:
            raise ValueError("Столбец с датами не найден")

        # Переименовываем столбец с датами в 'Дата'
        if date_column != 'Дата':
            df = df.rename(columns={date_column: 'Дата'})

        # Преобразуем столбец с датами
        df['Дата'] = pd.to_datetime(df['Дата'])

        # Устанавливаем дату как индекс
        df = df.set_index('Дата')

        # Проверяем наличие числовых столбцов
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_columns) == 0:
            raise ValueError("Не найдены числовые столбцы с данными")

        return df

    except Exception as e:
        st.error(f"Ошибка при загрузке данных: {str(e)}")
        return pd.DataFrame()


def filter_data_by_date(
    df: pd.DataFrame,
    start_date: Union[date, datetime],
    end_date: Union[date, datetime]
) -> pd.DataFrame:
    """
    Фильтрует DataFrame по диапазону дат.

    Args:
        df (pd.DataFrame): Исходный DataFrame с индексом-датой
        start_date (Union[date, datetime]): Начальная дата
        end_date (Union[date, datetime]): Конечная дата

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame
    """
    try:
        # Преобразуем даты в pandas timestamp для корректного сравнения
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        # Фильтруем данные по диапазону дат
        filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]

        return filtered_df

    except Exception as e:
        st.error(f"Ошибка при фильтрации данных: {str(e)}")
        return pd.DataFrame()


def get_date_range(df: pd.DataFrame) -> tuple[date, date]:
    """
    Получает диапазон дат из DataFrame.

    Args:
        df (pd.DataFrame): DataFrame с индексом-датой

    Returns:
        tuple[date, date]: Кортеж с минимальной и максимальной датами
    """
    try:
        if df.empty:
            # Возвращаем текущую дату как диапазон по умолчанию
            today = date.today()
            return today, today

        min_date = df.index.min().date()
        max_date = df.index.max().date()

        return min_date, max_date

    except Exception as e:
        st.error(f"Ошибка при получении диапазона дат: {str(e)}")
        today = date.today()
        return today, today


def validate_data(df: pd.DataFrame) -> bool:
    """
    Валидирует загруженные данные.

    Args:
        df (pd.DataFrame): DataFrame для валидации

    Returns:
        bool: True если данные валидны, False иначе
    """
    if df.empty:
        return False

    # Проверяем, что индекс содержит даты
    if not isinstance(df.index, pd.DatetimeIndex):
        return False

    # Проверяем наличие числовых данных
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) == 0:
        return False

    # Проверяем отсутствие отрицательных значений в данных о продажах
    for col in numeric_columns:
        if (df[col] < 0).any():
            st.warning(f"Обнаружены отрицательные значения в столбце {col}")

    return True


def prepare_data_summary(df: pd.DataFrame) -> dict:
    """
    Подготавливает сводку данных для отображения.

    Args:
        df (pd.DataFrame): DataFrame с данными

    Returns:
        dict: Словарь с информацией о данных
    """
    try:
        if df.empty:
            return {}

        summary = {
            'total_rows': len(df),
            'date_range': f"{df.index.min().strftime('%Y-%m-%d')} - {df.index.max().strftime('%Y-%m-%d')}",
            'columns': list(df.columns),
            'total_missing_values': df.isnull().sum().sum(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024  # в MB
        }

        return summary

    except Exception as e:
        st.error(f"Ошибка при подготовке сводки данных: {str(e)}")
        return {}


def validate_file_format(df: pd.DataFrame, uploaded_filename: Optional[str] = None) -> Dict[str, Union[bool, List[str]]]:
    """
    Валидирует формат загруженного файла.

    Args:
        df (pd.DataFrame): DataFrame для валидации
        uploaded_filename (Optional[str]): Имя загруженного файла

    Returns:
        Dict[str, Union[bool, List[str]]]: Результат валидации с деталями
    """
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'suggestions': []
    }

    try:
        if df.empty:
            validation_result['is_valid'] = False
            validation_result['errors'].append("Файл пустой или не содержит данных")
            return validation_result

        # Проверяем наличие столбца с датами
        date_columns = []
        first_col = df.columns[0] if len(df.columns) > 0 else None

        for col in df.columns:
            col_lower = str(col).lower()
            if ('дата' in col_lower or 'date' in col_lower or 'время' in col_lower or
                col == 'Unnamed: 0' or col == first_col):
                date_columns.append(col)

        # Всегда считаем первый столбец потенциальным столбцом с датами
        if first_col and first_col not in date_columns:
            # Проверяем, можно ли преобразовать первый столбец в даты
            try:
                pd.to_datetime(df[first_col].head())
                date_columns.append(first_col)
            except:
                pass

        if not date_columns:
            validation_result['errors'].append("Не найден столбец с датами. Ожидается столбец 'Дата', 'Date' или первый столбец с датами")
            validation_result['is_valid'] = False
        else:
            # Проверяем, что первый столбец можно преобразовать в даты
            try:
                pd.to_datetime(df[first_col])
            except:
                validation_result['warnings'].append(f"Первый столбец '{first_col}' может содержать некорректные даты")

        # Проверяем наличие числовых столбцов
        numeric_columns = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns
        if len(numeric_columns) == 0:
            validation_result['errors'].append("Не найдены столбцы с числовыми данными о продажах")
            validation_result['is_valid'] = False
        elif len(numeric_columns) < 2:
            validation_result['warnings'].append("Найден только один столбец с числовыми данными. Рекомендуется иметь несколько продуктов для сравнения")

        # Проверяем формат данных в первом столбце (даты)
        if len(df.columns) > 0:
            first_col = df.columns[0]
            try:
                # Пытаемся преобразовать в даты
                pd.to_datetime(df[first_col].head())
            except:
                if first_col not in date_columns:
                    validation_result['warnings'].append(f"Первый столбец '{first_col}' не распознан как дата")

        # Проверяем на отрицательные значения
        for col in numeric_columns:
            if (df[col] < 0).any():
                validation_result['warnings'].append(f"Столбец '{col}' содержит отрицательные значения")

        # Проверяем на пропущенные значения
        missing_data = df.isnull().sum()
        if missing_data.any():
            missing_cols = missing_data[missing_data > 0].index.tolist()
            validation_result['warnings'].append(f"Пропущенные значения в столбцах: {', '.join(missing_cols)}")

        # Добавляем рекомендации
        validation_result['suggestions'].extend([
            "Убедитесь, что первый столбец содержит даты в формате YYYY-MM-DD",
            "Числовые столбцы должны содержать данные о продажах или количестве сессий",
            "Рекомендуется использовать понятные названия столбцов (например: 'Продукт_1', 'Продукт_2')"
        ])

        return validation_result

    except Exception as e:
        validation_result['is_valid'] = False
        validation_result['errors'].append(f"Ошибка при валидации файла: {str(e)}")
        return validation_result


def get_file_format_requirements() -> Dict[str, str]:
    """
    Возвращает требования к формату файла.

    Returns:
        Dict[str, str]: Словарь с требованиями к формату
    """
    return {
        'file_types': 'Excel (.xlsx, .xls) или CSV (.csv)',
        'structure': 'Первый столбец - даты, остальные - числовые данные',
        'date_format': 'YYYY-MM-DD или стандартные форматы Excel',
        'encoding': 'UTF-8 (для CSV файлов)',
        'required_columns': 'Минимум 2 столбца: даты и числовые данные',
        'example_columns': 'Дата, Продукт_1, Продукт_2, Продукт_3',
        'data_requirements': 'Положительные числовые значения, без пропусков в датах'
    }