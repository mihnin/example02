#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тесты для рефакторенного модуля data_loader_refactored.py
"""

import sys
sys.path.append('.')

from data_loader_refactored import (
    load_sales_data,
    filter_data_by_date_range,
    get_date_range_from_dataframe,
    _determine_file_type,
    _find_date_column,
    _is_valid_date_column
)
import pandas as pd
from datetime import date
import tempfile
import os


def test_basic_functionality():
    """Тестирование базовой функциональности рефакторенного кода."""

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ РЕФАКТОРЕННОГО КОДА")
    print("=" * 60)

    # Тест 1: Загрузка демо данных
    print("\n1. Тестирование загрузки демо данных:")
    try:
        df = load_sales_data()
        if not df.empty:
            print(f"[OK] Успешно загружено {len(df)} строк")
            print(f"     Столбцы: {list(df.columns)}")
            print(f"     Период: {df.index.min().date()} - {df.index.max().date()}")
        else:
            print("[WARN] DataFrame пустой, но ошибки нет")
    except Exception as e:
        print(f"[ERROR] Ошибка при загрузке: {e}")
        return False

    # Тест 2: Получение диапазона дат
    print("\n2. Тестирование получения диапазона дат:")
    try:
        if not df.empty:
            min_date, max_date = get_date_range_from_dataframe(df)
            print(f"[OK] Диапазон дат: {min_date} - {max_date}")
        else:
            print("[SKIP] DataFrame пустой")
    except Exception as e:
        print(f"[ERROR] Ошибка получения диапазона: {e}")
        return False

    # Тест 3: Фильтрация по датам
    print("\n3. Тестирование фильтрации по датам:")
    try:
        if not df.empty:
            start_date = date(2020, 6, 1)
            end_date = date(2020, 12, 31)
            filtered_df = filter_data_by_date_range(df, start_date, end_date)
            print(f"[OK] Отфильтровано {len(filtered_df)} строк из {len(df)}")
            if not filtered_df.empty:
                print(f"     Период фильтра: {filtered_df.index.min().date()} - {filtered_df.index.max().date()}")
        else:
            print("[SKIP] DataFrame пустой для фильтрации")
    except Exception as e:
        print(f"[ERROR] Ошибка фильтрации: {e}")
        return False

    return True


def test_helper_functions():
    """Тестирование вспомогательных функций."""

    print("\n4. Тестирование вспомогательных функций:")

    # Тест определения типа файла
    try:
        # Создаем mock объект для тестирования
        class MockFile:
            def __init__(self, name):
                self.name = name

        excel_file = MockFile("test.xlsx")
        csv_file = MockFile("test.csv")

        assert _determine_file_type(excel_file) == 'excel'
        assert _determine_file_type(csv_file) == 'csv'
        print("[OK] Определение типа файла работает корректно")

    except Exception as e:
        print(f"[ERROR] Ошибка определения типа файла: {e}")
        return False

    # Тест поиска столбца с датами
    try:
        # Создаем тестовый DataFrame
        test_df = pd.DataFrame({
            'Дата': ['2020-01-01', '2020-01-02', '2020-01-03'],
            'Продукт_1': [100, 120, 110],
            'Продукт_2': [80, 90, 85]
        })

        date_column = _find_date_column(test_df)
        assert date_column == 'Дата'
        print("[OK] Поиск столбца с датами работает корректно")

    except Exception as e:
        print(f"[ERROR] Ошибка поиска столбца с датами: {e}")
        return False

    # Тест валидации столбца с датами
    try:
        test_df = pd.DataFrame({
            'valid_dates': ['2020-01-01', '2020-01-02', '2020-01-03'],
            'invalid_dates': ['not_a_date', 'also_not_date', 'nope']
        })

        assert _is_valid_date_column(test_df, 'valid_dates') == True
        assert _is_valid_date_column(test_df, 'invalid_dates') == False
        print("[OK] Валидация столбца с датами работает корректно")

    except Exception as e:
        print(f"[ERROR] Ошибка валидации дат: {e}")
        return False

    return True


def test_error_handling():
    """Тестирование обработки ошибок."""

    print("\n5. Тестирование обработки ошибок:")

    # Тест с пустым DataFrame
    try:
        empty_df = pd.DataFrame()
        min_date, max_date = get_date_range_from_dataframe(empty_df)
        print("[OK] Обработка пустого DataFrame работает корректно")
    except Exception as e:
        print(f"[ERROR] Ошибка обработки пустого DataFrame: {e}")
        return False

    # Тест с неверным диапазоном дат
    try:
        df = load_sales_data()
        if not df.empty:
            # Неверный диапазон: конечная дата раньше начальной
            start_date = date(2020, 12, 31)
            end_date = date(2020, 6, 1)
            filtered_df = filter_data_by_date_range(df, start_date, end_date)
            print("[OK] Обработка неверного диапазона дат работает корректно")
    except Exception as e:
        print(f"[ERROR] Ошибка обработки неверного диапазона: {e}")
        return False

    return True


def main():
    """Главная функция тестирования."""

    all_tests_passed = True

    # Запускаем все тесты
    all_tests_passed &= test_basic_functionality()
    all_tests_passed &= test_helper_functions()
    all_tests_passed &= test_error_handling()

    # Итоговые результаты
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("РЕЗУЛЬТАТ: ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("Рефакторенный код работает корректно.")
    else:
        print("РЕЗУЛЬТАТ: НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ!")
        print("Требуется доработка кода.")
    print("=" * 60)

    return all_tests_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)