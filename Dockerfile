# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip3 install -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Открываем порт для Streamlit
EXPOSE 8501

# Проверяем зависимости
RUN python check_dependencies.py

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app
USER app

# Команда запуска
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]