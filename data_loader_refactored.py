"""
Рефакторенный модуль для загрузки и обработки данных о продажах.

Этот модуль содержит функции для загрузки данных из различных источников
с улучшенной архитектурой и разделением ответственности.
"""

import pandas as pd
import streamlit as st
from datetime import datetime, date
from typing import Optional, Union, Dict, List, Tuple
import os
from pathlib import Path


# Константы для улучшения читаемости
SUPPORTED_FILE_EXTENSIONS = {'.xlsx', '.xls', '.csv'}
DATE_COLUMN_INDICATORS = {'дата', 'date', 'время', 'unnamed: 0'}
DEFAULT_DATE_COLUMN_NAME = 'Дата'
DEFAULT_DATA_PATH = "docs/sample_sales_data.xlsx"
NUMERIC_DTYPES = ['int64', 'float64']


def _determine_file_type(file_source: Union[str, object]) -> str:
    """
    Определяет тип файла на основе расширения.

    Args:
        file_source (Union[str, object]): Путь к файлу или объект загруженного файла

    Returns:
        str: Тип файла ('excel' или 'csv')

    Raises:
        ValueError: Если формат файла не поддерживается
    """
    if hasattr(file_source, 'name'):
        filename = file_source.name
    else:
        filename = str(file_source)

    file_extension = Path(filename).suffix.lower()

    if file_extension in {'.xlsx', '.xls'}:
        return 'excel'
    elif file_extension == '.csv':
        return 'csv'
    else:
        raise ValueError(
            f"Неподдерживаемый формат файла: {file_extension}. "
            f"Поддерживаются: {', '.join(SUPPORTED_FILE_EXTENSIONS)}"
        )


def _load_dataframe_from_source(
    file_path: Optional[str] = None,
    uploaded_file: Optional[object] = None
) -> pd.DataFrame:
    """
    Загружает DataFrame из указанного источника данных.

    Args:
        file_path (Optional[str]): Путь к локальному файлу
        uploaded_file (Optional[object]): Загруженный файл из Streamlit

    Returns:
        pd.DataFrame: Загруженный DataFrame

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если формат файла не поддерживается
    """
    if uploaded_file is not None:
        return _read_uploaded_file(uploaded_file)
    elif file_path is not None:
        return _read_local_file(file_path)
    else:
        return _read_default_file()


def _read_uploaded_file(uploaded_file: object) -> pd.DataFrame:
    """
    Читает данные из загруженного файла.

    Args:
        uploaded_file (object): Объект загруженного файла из Streamlit

    Returns:
        pd.DataFrame: DataFrame с данными из файла

    Raises:
        ValueError: Если формат файла не поддерживается
    """
    file_type = _determine_file_type(uploaded_file)

    if file_type == 'excel':
        return pd.read_excel(uploaded_file)
    elif file_type == 'csv':
        return pd.read_csv(uploaded_file)


def _read_local_file(file_path: str) -> pd.DataFrame:
    """
    Читает данные из локального файла.

    Args:
        file_path (str): Путь к локальному файлу

    Returns:
        pd.DataFrame: DataFrame с данными из файла

    Raises:
        FileNotFoundError: Если файл не найден
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    return pd.read_excel(file_path)


def _read_default_file() -> pd.DataFrame:
    """
    Читает данные из файла по умолчанию.

    Returns:
        pd.DataFrame: DataFrame с демонстрационными данными

    Raises:
        FileNotFoundError: Если файл по умолчанию не найден
    """
    if os.path.exists(DEFAULT_DATA_PATH):
        return pd.read_excel(DEFAULT_DATA_PATH)
    else:
        raise FileNotFoundError(
            "Файл данных не найден. Пожалуйста, загрузите файл."
        )


def _find_date_column(dataframe: pd.DataFrame) -> Optional[str]:
    """
    Находит столбец с датами в DataFrame.

    Args:
        dataframe (pd.DataFrame): DataFrame для анализа

    Returns:
        Optional[str]: Название столбца с датами или None, если не найден
    """
    # Ищем столбец по названию
    for column_name in dataframe.columns:
        normalized_name = str(column_name).lower()
        if any(indicator in normalized_name for indicator in DATE_COLUMN_INDICATORS):
            return column_name

    # Если не нашли по названию, проверяем первый столбец
    first_column = dataframe.columns[0] if len(dataframe.columns) > 0 else None
    if first_column is not None and _is_valid_date_column(dataframe, first_column):
        return first_column

    return None


def _is_valid_date_column(dataframe: pd.DataFrame, column_name: str) -> bool:
    """
    Проверяет, содержит ли столбец валидные даты.

    Args:
        dataframe (pd.DataFrame): DataFrame для проверки
        column_name (str): Название столбца для проверки

    Returns:
        bool: True, если столбец содержит валидные даты
    """
    try:
        pd.to_datetime(dataframe[column_name].head())
        return True
    except (ValueError, TypeError):
        return False


def _normalize_date_column(
    dataframe: pd.DataFrame,
    date_column_name: str
) -> pd.DataFrame:
    """
    Нормализует столбец с датами и устанавливает его как индекс.

    Args:
        dataframe (pd.DataFrame): Исходный DataFrame
        date_column_name (str): Название столбца с датами

    Returns:
        pd.DataFrame: DataFrame с нормализованным индексом дат

    Raises:
        ValueError: Если не удается преобразовать столбец в даты
    """
    processed_df = dataframe.copy()

    # Переименовываем столбец, если необходимо
    if date_column_name != DEFAULT_DATE_COLUMN_NAME:
        processed_df = processed_df.rename(
            columns={date_column_name: DEFAULT_DATE_COLUMN_NAME}
        )

    # Преобразуем в даты
    try:
        processed_df[DEFAULT_DATE_COLUMN_NAME] = pd.to_datetime(
            processed_df[DEFAULT_DATE_COLUMN_NAME]
        )
    except (ValueError, TypeError) as e:
        raise ValueError(f"Не удается преобразовать столбец в даты: {str(e)}")

    # Устанавливаем как индекс
    processed_df = processed_df.set_index(DEFAULT_DATE_COLUMN_NAME)

    return processed_df


def _validate_numeric_columns(dataframe: pd.DataFrame) -> None:
    """
    Проверяет наличие числовых столбцов в DataFrame.

    Args:
        dataframe (pd.DataFrame): DataFrame для проверки

    Raises:
        ValueError: Если числовые столбцы не найдены
    """
    numeric_columns = dataframe.select_dtypes(include=NUMERIC_DTYPES).columns
    if len(numeric_columns) == 0:
        raise ValueError("Не найдены числовые столбцы с данными")


def _process_sales_dataframe(raw_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Обрабатывает сырой DataFrame для анализа продаж.

    Args:
        raw_dataframe (pd.DataFrame): Исходный DataFrame

    Returns:
        pd.DataFrame: Обработанный DataFrame с датами как индекс

    Raises:
        ValueError: Если данные имеют неверный формат
    """
    # Находим столбец с датами
    date_column = _find_date_column(raw_dataframe)
    if date_column is None:
        raise ValueError("Столбец с датами не найден")

    # Нормализуем даты и устанавливаем индекс
    processed_df = _normalize_date_column(raw_dataframe, date_column)

    # Проверяем наличие числовых данных
    _validate_numeric_columns(processed_df)

    return processed_df


@st.cache_data
def load_sales_data(
    file_path: Optional[str] = None,
    uploaded_file: Optional[object] = None
) -> pd.DataFrame:
    """
    Загружает и обрабатывает данные о продажах с кэшированием.

    Функция поддерживает загрузку из различных источников:
    - Загруженный пользователем файл (Excel/CSV)
    - Локальный файл по указанному пути
    - Файл демонстрационных данных по умолчанию

    Args:
        file_path (Optional[str]): Путь к локальному файлу с данными
        uploaded_file (Optional[object]): Загруженный файл из Streamlit

    Returns:
        pd.DataFrame: DataFrame с данными о продажах, где:
            - Индекс: даты (pandas DatetimeIndex)
            - Столбцы: числовые данные о продажах/сессиях

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если данные имеют неверный формат

    Example:
        >>> # Загрузка демонстрационных данных
        >>> df = load_sales_data()
        >>>
        >>> # Загрузка из локального файла
        >>> df = load_sales_data(file_path="data/sales.xlsx")
        >>>
        >>> # Обработка загруженного файла
        >>> df = load_sales_data(uploaded_file=streamlit_uploaded_file)
    """
    try:
        # Загружаем сырые данные
        raw_dataframe = _load_dataframe_from_source(file_path, uploaded_file)

        # Обрабатываем для анализа
        processed_dataframe = _process_sales_dataframe(raw_dataframe)

        return processed_dataframe

    except Exception as e:
        st.error(f"Ошибка при загрузке данных: {str(e)}")
        return pd.DataFrame()


def filter_data_by_date_range(
    dataframe: pd.DataFrame,
    start_date: Union[date, datetime],
    end_date: Union[date, datetime]
) -> pd.DataFrame:
    """
    Фильтрует DataFrame по диапазону дат с улучшенной обработкой ошибок.

    Args:
        dataframe (pd.DataFrame): DataFrame с индексом-датой
        start_date (Union[date, datetime]): Начальная дата диапазона
        end_date (Union[date, datetime]): Конечная дата диапазона

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame

    Raises:
        ValueError: Если даты имеют неверный формат или диапазон пустой
    """
    try:
        if dataframe.empty:
            return dataframe

        # Нормализуем даты
        normalized_start = pd.Timestamp(start_date)
        normalized_end = pd.Timestamp(end_date)

        # Проверяем корректность диапазона
        if normalized_start > normalized_end:
            raise ValueError("Начальная дата не может быть позже конечной")

        # Фильтруем данные
        date_mask = (
            (dataframe.index >= normalized_start) &
            (dataframe.index <= normalized_end)
        )
        filtered_dataframe = dataframe[date_mask]

        return filtered_dataframe

    except Exception as e:
        st.error(f"Ошибка при фильтрации данных: {str(e)}")
        return pd.DataFrame()


def get_date_range_from_dataframe(dataframe: pd.DataFrame) -> Tuple[date, date]:
    """
    Извлекает диапазон дат из DataFrame с улучшенной обработкой ошибок.

    Args:
        dataframe (pd.DataFrame): DataFrame с индексом-датой

    Returns:
        Tuple[date, date]: Кортеж с минимальной и максимальной датами

    Example:
        >>> min_date, max_date = get_date_range_from_dataframe(df)
        >>> print(f"Данные доступны с {min_date} по {max_date}")
    """
    try:
        if dataframe.empty:
            current_date = date.today()
            return current_date, current_date

        min_date = dataframe.index.min().date()
        max_date = dataframe.index.max().date()

        return min_date, max_date

    except Exception as e:
        st.error(f"Ошибка при получении диапазона дат: {str(e)}")
        current_date = date.today()
        return current_date, current_date