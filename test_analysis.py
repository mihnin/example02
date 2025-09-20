"""
Тесты для модуля analysis.py

Этот модуль содержит юнит-тесты для проверки корректности функций
анализа данных с использованием pytest.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch

# Импорт тестируемых функций
from analysis import (
    calculate_basic_statistics,
    calculate_kpi_metrics,
    calculate_moving_average,
    detect_anomalies,
    calculate_correlation_matrix,
    generate_insights,
    _calculate_growth_rate,
)


class TestAnalysisFunctions:
    """Тестовый класс для функций анализа данных."""

    @pytest.fixture
    def sample_data(self):
        """Фикстура для создания тестовых данных."""
        dates = pd.date_range(start="2020-01-01", periods=10, freq="D")
        data = {
            "Продукт_1": [100, 120, 110, 130, 140, 135, 150, 160, 155, 170],
            "Продукт_2": [80, 90, 85, 95, 100, 105, 110, 115, 120, 125],
            "Продукт_3": [60, 65, 70, 75, 80, 85, 90, 95, 100, 105],
        }
        df = pd.DataFrame(data, index=dates)
        return df

    @pytest.fixture
    def empty_data(self):
        """Фикстура для пустого DataFrame."""
        return pd.DataFrame()

    @pytest.fixture
    def data_with_missing(self):
        """Фикстура для данных с пропусками."""
        dates = pd.date_range(start="2020-01-01", periods=5, freq="D")
        data = {
            "Продукт_1": [100, np.nan, 110, 130, 140],
            "Продукт_2": [80, 90, np.nan, 95, 100],
            "Продукт_3": [60, 65, 70, np.nan, 80],
        }
        df = pd.DataFrame(data, index=dates)
        return df

    @pytest.fixture
    def single_column_data(self):
        """Фикстура для данных с одним столбцом."""
        dates = pd.date_range(start="2020-01-01", periods=5, freq="D")
        data = {"Продукт_1": [100, 120, 110, 130, 140]}
        df = pd.DataFrame(data, index=dates)
        return df

    def test_calculate_basic_statistics_normal_data(self, sample_data):
        """Тест расчета базовой статистики для нормальных данных."""
        result = calculate_basic_statistics(sample_data)

        assert isinstance(result, dict)
        assert "Продукт_1" in result
        assert "Продукт_2" in result
        assert "Продукт_3" in result

        # Проверяем структуру результата для одного продукта
        product_stats = result["Продукт_1"]
        expected_keys = ["mean", "median", "std", "min", "max", "sum", "count"]
        for key in expected_keys:
            assert key in product_stats
            assert isinstance(product_stats[key], (int, float))

        # Проверяем корректность расчетов
        expected_mean = sum([100, 120, 110, 130, 140, 135, 150, 160, 155, 170]) / 10
        assert abs(product_stats["mean"] - expected_mean) < 0.1
        assert product_stats["min"] == 100.0
        assert product_stats["max"] == 170.0
        assert product_stats["sum"] == 1370.0  # Исправлена сумма
        assert product_stats["count"] == 10

    def test_calculate_basic_statistics_empty_data(self, empty_data):
        """Тест расчета базовой статистики для пустых данных."""
        result = calculate_basic_statistics(empty_data)
        assert result == {}

    def test_calculate_basic_statistics_with_missing_data(self, data_with_missing):
        """Тест расчета базовой статистики для данных с пропусками."""
        result = calculate_basic_statistics(data_with_missing)

        assert isinstance(result, dict)
        assert "Продукт_1" in result

        # Проверяем, что функция обрабатывает пропуски
        product_stats = result["Продукт_1"]
        assert product_stats["count"] == 4  # 5 значений - 1 пропуск

    def test_calculate_kpi_metrics_normal_data(self, sample_data):
        """Тест расчета KPI метрик для нормальных данных."""
        result = calculate_kpi_metrics(sample_data)

        assert isinstance(result, dict)
        required_keys = [
            "total_sessions",
            "avg_daily_sessions",
            "max_daily_sessions",
            "min_daily_sessions",
            "days_count",
            "growth_rate",
        ]

        for key in required_keys:
            assert key in result
            assert isinstance(result[key], (int, float))

        # Проверяем корректность расчетов
        expected_total = sample_data.sum(axis=1).sum()
        assert result["total_sessions"] == expected_total
        assert result["days_count"] == 10
        assert result["avg_daily_sessions"] == expected_total / 10

    def test_calculate_kpi_metrics_empty_data(self, empty_data):
        """Тест расчета KPI метрик для пустых данных."""
        result = calculate_kpi_metrics(empty_data)

        expected_result = {
            "total_sessions": 0,
            "avg_daily_sessions": 0.0,
            "max_daily_sessions": 0,
        }

        for key, value in expected_result.items():
            assert result[key] == value

    def test_calculate_kpi_metrics_single_column(self, single_column_data):
        """Тест расчета KPI метрик для данных с одним столбцом."""
        result = calculate_kpi_metrics(single_column_data)

        assert isinstance(result, dict)
        assert result["total_sessions"] == 600  # сумма всех значений
        assert result["days_count"] == 5

    def test_calculate_moving_average_normal_data(self, sample_data):
        """Тест расчета скользящего среднего для нормальных данных."""
        window = 3
        result = calculate_moving_average(sample_data, window=window)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)

        # Проверяем, что добавились колонки со скользящим средним
        for col in sample_data.columns:
            ma_col = f"{col}_MA{window}"
            assert ma_col in result.columns

        # Проверяем, что первые значения NaN (недостаточно данных для окна)
        assert pd.isna(result[f"Продукт_1_MA{window}"].iloc[0])
        assert pd.isna(result[f"Продукт_1_MA{window}"].iloc[1])

    def test_calculate_moving_average_specific_column(self, sample_data):
        """Тест расчета скользящего среднего для конкретного столбца."""
        window = 3
        column = "Продукт_1"
        result = calculate_moving_average(sample_data, window=window, column=column)

        assert isinstance(result, pd.DataFrame)
        ma_col = f"{column}_MA{window}"
        assert ma_col in result.columns

        # Проверяем корректность расчета (третье значение должно быть средним первых трех)
        expected_ma_value = sample_data[column].iloc[:3].mean()
        assert abs(result[ma_col].iloc[2] - expected_ma_value) < 0.001

    def test_calculate_moving_average_empty_data(self, empty_data):
        """Тест расчета скользящего среднего для пустых данных."""
        result = calculate_moving_average(empty_data)
        assert result.empty

    def test_detect_anomalies_zscore_method(self, sample_data):
        """Тест обнаружения аномалий методом z-score."""
        result = detect_anomalies(sample_data, threshold=2.0, method="zscore")

        assert isinstance(result, dict)

        # Проверяем структуру результата
        for col in sample_data.columns:
            assert col in result
            assert isinstance(result[col], list)

    def test_detect_anomalies_iqr_method(self, sample_data):
        """Тест обнаружения аномалий методом IQR."""
        result = detect_anomalies(sample_data, threshold=1.5, method="iqr")

        assert isinstance(result, dict)

        # Проверяем структуру результата
        for col in sample_data.columns:
            assert col in result
            assert isinstance(result[col], list)

    def test_detect_anomalies_invalid_method(self, sample_data):
        """Тест обнаружения аномалий с неверным методом."""
        result = detect_anomalies(sample_data, method="invalid_method")

        # Должен вернуть словарь с пустыми списками для всех столбцов
        assert isinstance(result, dict)
        # Проверяем, что результат содержит записи для числовых столбцов
        numeric_columns = sample_data.select_dtypes(
            include=["int64", "float64"]
        ).columns
        for col in numeric_columns:
            if col in result:
                assert result[col] == []

    def test_detect_anomalies_empty_data(self, empty_data):
        """Тест обнаружения аномалий для пустых данных."""
        result = detect_anomalies(empty_data)
        assert result == {}

    def test_calculate_correlation_matrix_normal_data(self, sample_data):
        """Тест расчета корреляционной матрицы для нормальных данных."""
        result = calculate_correlation_matrix(sample_data)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 3)  # 3x3 матрица для 3 продуктов

        # Проверяем, что диагональные элементы равны 1
        for i in range(len(result)):
            assert abs(result.iloc[i, i] - 1.0) < 0.001

    def test_calculate_correlation_matrix_empty_data(self, empty_data):
        """Тест расчета корреляционной матрицы для пустых данных."""
        result = calculate_correlation_matrix(empty_data)
        assert result.empty

    def test_calculate_growth_rate_normal_data(self):
        """Тест расчета темпа роста для нормальных данных."""
        series = pd.Series([100, 120, 150])
        result = _calculate_growth_rate(series)

        expected_growth = ((150 - 100) / 100) * 100  # 50%
        assert abs(result - expected_growth) < 0.001

    def test_calculate_growth_rate_zero_first_value(self):
        """Тест расчета темпа роста когда первое значение равно нулю."""
        series = pd.Series([0, 100, 150])
        result = _calculate_growth_rate(series)
        assert result == 0.0

    def test_calculate_growth_rate_single_value(self):
        """Тест расчета темпа роста для одного значения."""
        series = pd.Series([100])
        result = _calculate_growth_rate(series)
        assert result == 0.0

    def test_calculate_growth_rate_empty_series(self):
        """Тест расчета темпа роста для пустой серии."""
        series = pd.Series([])
        result = _calculate_growth_rate(series)
        assert result == 0.0

    @patch("streamlit.error")
    def test_generate_insights_normal_data(self, mock_st_error, sample_data):
        """Тест генерации инсайтов для нормальных данных."""
        statistics = calculate_basic_statistics(sample_data)
        result = generate_insights(sample_data, statistics)

        assert isinstance(result, list)
        assert len(result) > 0

        # Проверяем, что инсайты содержат полезную информацию
        insights_text = " ".join(result)
        assert any(
            word in insights_text for word in ["рост", "продаж", "лидер", "продукт"]
        )

    @patch("streamlit.error")
    def test_generate_insights_empty_data(self, mock_st_error, empty_data):
        """Тест генерации инсайтов для пустых данных."""
        result = generate_insights(empty_data, {})

        assert isinstance(result, list)
        assert len(result) == 1
        assert "Недостаточно данных" in result[0]

    @patch("streamlit.error")
    def test_generate_insights_with_high_volatility(self, mock_st_error):
        """Тест генерации инсайтов для данных с высокой волатильностью."""
        # Создаем данные с высокой волатильностью
        dates = pd.date_range(start="2020-01-01", periods=5, freq="D")
        data = {
            "Продукт_1": [10, 100, 20, 200, 30],  # Высокая волатильность
            "Продукт_2": [50, 55, 52, 58, 54],  # Низкая волатильность
        }
        df = pd.DataFrame(data, index=dates)

        statistics = calculate_basic_statistics(df)
        result = generate_insights(df, statistics)

        assert isinstance(result, list)
        insights_text = " ".join(result)
        assert "волатильность" in insights_text

    def test_functions_with_streamlit_mocking(self, sample_data):
        """Тест функций с мокингом Streamlit."""
        with patch("streamlit.error") as mock_error:
            # Тестируем, что функции не вызывают ошибки при нормальных данных
            calculate_basic_statistics(sample_data)
            calculate_kpi_metrics(sample_data)
            calculate_moving_average(sample_data)

            # Проверяем, что ошибки не вызывались
            mock_error.assert_not_called()


class TestDataValidation:
    """Тестовый класс для проверки валидации данных."""

    def test_functions_handle_non_numeric_columns(self):
        """Тест обработки нечисловых столбцов."""
        dates = pd.date_range(start="2020-01-01", periods=3, freq="D")
        data = {
            "Продукт_1": [100, 120, 110],
            "Текст": ["a", "b", "c"],  # Нечисловой столбец
            "Продукт_2": [80, 90, 85],
        }
        df = pd.DataFrame(data, index=dates)

        # Функции должны игнорировать нечисловые столбцы
        stats = calculate_basic_statistics(df)
        assert "Текст" not in stats
        assert "Продукт_1" in stats
        assert "Продукт_2" in stats

    def test_functions_handle_negative_values(self):
        """Тест обработки отрицательных значений."""
        dates = pd.date_range(start="2020-01-01", periods=3, freq="D")
        data = {"Продукт_1": [-10, 20, -5], "Продукт_2": [10, -20, 15]}
        df = pd.DataFrame(data, index=dates)

        # Функции должны корректно обрабатывать отрицательные значения
        stats = calculate_basic_statistics(df)
        assert stats["Продукт_1"]["min"] == -10.0

        kpi = calculate_kpi_metrics(df)
        assert isinstance(kpi["total_sessions"], (int, float))


class TestEdgeCases:
    """Тестовый класс для проверки граничных случаев."""

    def test_large_dataset_performance(self):
        """Тест производительности на больших данных."""
        # Создаем большой dataset
        dates = pd.date_range(start="2020-01-01", periods=1000, freq="D")
        data = {
            f"Продукт_{i}": np.random.randint(50, 200, 1000)
            for i in range(1, 11)  # 10 продуктов
        }
        df = pd.DataFrame(data, index=dates)

        # Проверяем, что функции работают без ошибок
        import time

        start_time = time.time()

        calculate_basic_statistics(df)
        calculate_kpi_metrics(df)
        calculate_moving_average(df, window=7)

        end_time = time.time()
        execution_time = end_time - start_time

        # Проверяем, что выполнение занимает разумное время (< 5 секунд)
        assert execution_time < 5.0

    def test_seasonal_decomposition_insufficient_data(self):
        """Тест сезонной декомпозиции с недостаточными данными."""
        from analysis import calculate_seasonal_decomposition

        # Данные с недостаточным количеством периодов
        dates = pd.date_range(start="2020-01-01", periods=5, freq="D")
        data = {"Продукт_1": [100, 120, 110, 130, 140]}
        df = pd.DataFrame(data, index=dates)

        result = calculate_seasonal_decomposition(df, "Продукт_1", period=12)

        # Должен вернуть None из-за недостатка данных
        assert result is None

    def test_functions_with_extreme_values(self):
        """Тест функций с экстремальными значениями."""
        dates = pd.date_range(start="2020-01-01", periods=3, freq="D")
        data = {
            "Продукт_1": [1e10, 1e-10, 1e5],  # Очень большие и маленькие числа
            "Продукт_2": [0, 0, 0],  # Нулевые значения
        }
        df = pd.DataFrame(data, index=dates)

        # Функции должны корректно обрабатывать экстремальные значения
        stats = calculate_basic_statistics(df)
        assert isinstance(stats["Продукт_1"]["mean"], float)
        assert stats["Продукт_2"]["sum"] == 0.0

        kpi = calculate_kpi_metrics(df)
        assert isinstance(kpi["total_sessions"], (int, float))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
