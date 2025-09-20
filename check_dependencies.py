#!/usr/bin/env python3
"""
Скрипт для проверки всех необходимых зависимостей.
"""

import sys

def check_import(module_name, package_name=None):
    """Проверяет возможность импорта модуля."""
    try:
        __import__(module_name)
        print(f"[OK] {package_name or module_name} - установлен")
        return True
    except ImportError as e:
        print(f"[ERROR] {package_name or module_name} - НЕ УСТАНОВЛЕН")
        print(f"   Ошибка: {e}")
        return False

def main():
    """Основная функция проверки."""
    print("Проверка зависимостей для Streamlit приложения...")
    print("=" * 50)

    dependencies = [
        ("streamlit", "Streamlit"),
        ("plotly.express", "Plotly"),
        ("pandas", "Pandas"),
        ("openpyxl", "OpenPyXL"),
        ("statsmodels", "Statsmodels"),
        ("numpy", "NumPy"),
        ("dateutil", "python-dateutil")
    ]

    all_ok = True
    for module, name in dependencies:
        if not check_import(module, name):
            all_ok = False

    print("=" * 50)
    if all_ok:
        print("SUCCESS: Все зависимости установлены корректно!")
        print("Приложение готово к запуску: streamlit run app.py")
    else:
        print("WARNING: Обнаружены отсутствующие зависимости!")
        print("Установите их командой: pip install -r requirements.txt")

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())