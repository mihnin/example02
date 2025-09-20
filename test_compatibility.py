"""
Тесты совместимости для рефакторенного модуля.
Проверяет, что рефакторенный код имеет тот же API что и оригинальный.
"""

import pytest
import pandas as pd
from unittest.mock import patch

# Импорты оригинального и рефакторенного модулей
from data_loader import load_sales_data as original_load_sales_data
from data_loader_refactored import load_sales_data as refactored_load_sales_data


class TestCompatibility:
    """Тесты совместимости API между оригинальным и рефакторенным кодом."""

    def test_load_sales_data_signature_compatibility(self):
        """Тест совместимости сигнатуры функции load_sales_data."""

        # Проверяем, что обе функции принимают одинаковые параметры
        import inspect

        original_sig = inspect.signature(original_load_sales_data)
        refactored_sig = inspect.signature(refactored_load_sales_data)

        # Параметры должны совпадать
        assert len(original_sig.parameters) == len(refactored_sig.parameters)

        for param_name in original_sig.parameters:
            assert param_name in refactored_sig.parameters

    @patch("streamlit.error")
    def test_load_sales_data_return_type_compatibility(self, mock_st_error):
        """Тест совместимости возвращаемого типа."""

        # Обе функции должны возвращать DataFrame
        original_result = original_load_sales_data()
        refactored_result = refactored_load_sales_data()

        assert isinstance(original_result, pd.DataFrame)
        assert isinstance(refactored_result, pd.DataFrame)

    @patch("streamlit.error")
    def test_load_sales_data_structure_compatibility(self, mock_st_error):
        """Тест совместимости структуры возвращаемых данных."""

        original_result = original_load_sales_data()
        refactored_result = refactored_load_sales_data()

        # Если оба DataFrame не пустые, проверяем структуру
        if not original_result.empty and not refactored_result.empty:
            # Количество строк должно совпадать
            assert len(original_result) == len(refactored_result)

            # Количество столбцов должно совпадать
            assert len(original_result.columns) == len(refactored_result.columns)

            # Типы индексов должны совпадать
            assert isinstance(original_result.index, type(refactored_result.index))

            # Столбцы должны быть одинаковыми (порядок может отличаться)
            assert set(original_result.columns) == set(refactored_result.columns)

    @patch("streamlit.error")
    def test_data_content_compatibility(self, mock_st_error):
        """Тест совместимости содержимого данных."""

        original_result = original_load_sales_data()
        refactored_result = refactored_load_sales_data()

        # Если оба DataFrame не пустые, проверяем данные
        if not original_result.empty and not refactored_result.empty:
            # Сортируем по индексу для корректного сравнения
            original_sorted = original_result.sort_index()
            refactored_sorted = refactored_result.sort_index()

            # Данные должны быть идентичными
            pd.testing.assert_frame_equal(
                original_sorted,
                refactored_sorted,
                check_dtype=False,  # Позволяем небольшие различия в типах
            )

    def test_error_handling_compatibility(self):
        """Тест совместимости обработки ошибок."""

        # Обе функции должны возвращать пустой DataFrame при ошибках
        # а не выбрасывать исключения
        with patch("os.path.exists", return_value=False):
            original_result = original_load_sales_data("nonexistent_file.xlsx")
            refactored_result = refactored_load_sales_data("nonexistent_file.xlsx")

            assert isinstance(original_result, pd.DataFrame)
            assert isinstance(refactored_result, pd.DataFrame)
            assert original_result.empty
            assert refactored_result.empty


class TestPerformance:
    """Тесты производительности рефакторенного кода."""

    @patch("streamlit.error")
    def test_performance_comparison(self, mock_st_error):
        """Сравнение производительности оригинального и рефакторенного кода."""

        import time

        # Измеряем время выполнения оригинального кода
        start_time = time.time()
        for _ in range(5):  # 5 итераций
            original_load_sales_data()
        original_time = time.time() - start_time

        # Измеряем время выполнения рефакторенного кода
        start_time = time.time()
        for _ in range(5):  # 5 итераций
            refactored_load_sales_data()
        refactored_time = time.time() - start_time

        # Рефакторенный код не должен быть значительно медленнее
        # Допускаем 20% замедление из-за дополнительных проверок
        assert refactored_time <= original_time * 1.2, (
            f"Рефакторенный код слишком медленный: "
            f"{refactored_time:.3f}s vs {original_time:.3f}s"
        )

        print(f"Оригинальный код: {original_time:.3f}s")
        print(f"Рефакторенный код: {refactored_time:.3f}s")
        print(
            f"Изменение: {((refactored_time - original_time) / original_time * 100):+.1f}%"
        )


class TestCodeQuality:
    """Тесты качества рефакторенного кода."""

    def test_function_length(self):
        """Проверяет, что функции имеют разумную длину."""

        import inspect
        from data_loader_refactored import (
            load_sales_data,
            _determine_file_type,
            _load_dataframe_from_source,
            _read_uploaded_file,
            _read_local_file,
            _read_default_file,
            _find_date_column,
            _is_valid_date_column,
            _normalize_date_column,
        )

        functions_to_test = [
            load_sales_data,
            _determine_file_type,
            _load_dataframe_from_source,
            _read_uploaded_file,
            _read_local_file,
            _read_default_file,
            _find_date_column,
            _is_valid_date_column,
            _normalize_date_column,
        ]

        for func in functions_to_test:
            source_lines = inspect.getsource(func).split("\n")
            # Убираем пустые строки и комментарии
            code_lines = [
                line
                for line in source_lines
                if line.strip() and not line.strip().startswith("#")
            ]

            # Каждая функция должна быть не более 50 строк кода
            assert (
                len(code_lines) <= 50
            ), f"Функция {func.__name__} слишком длинная: {len(code_lines)} строк"

    def test_docstring_presence(self):
        """Проверяет наличие docstring у всех публичных функций."""

        from data_loader_refactored import (
            load_sales_data,
            filter_data_by_date_range,
            get_date_range_from_dataframe,
        )

        public_functions = [
            load_sales_data,
            filter_data_by_date_range,
            get_date_range_from_dataframe,
        ]

        for func in public_functions:
            assert (
                func.__doc__ is not None
            ), f"Функция {func.__name__} не имеет docstring"
            assert (
                len(func.__doc__.strip()) > 50
            ), f"Docstring функции {func.__name__} слишком короткий"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
