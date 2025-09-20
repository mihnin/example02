# Docker Deployment Guide

## Быстрый запуск | Quick Start

### Сборка и запуск контейнера | Build and Run Container

```bash
# Сборка образа | Build image
docker build -t streamlit-analyzer .

# Запуск контейнера | Run container
docker run -d -p 8502:8501 --name streamlit-app streamlit-analyzer

# Проверка статуса | Check status
docker ps

# Просмотр логов | View logs
docker logs streamlit-app
```

### Доступ к приложению | Access Application

Приложение будет доступно по адресу: **http://localhost:8502**

Application will be available at: **http://localhost:8502**


### Управление контейнером | Container Management

```bash
# Остановка контейнера | Stop container
docker stop streamlit-app

# Запуск существующего контейнера | Start existing container
docker start streamlit-app

# Удаление контейнера | Remove container
docker rm streamlit-app

# Удаление образа | Remove image
docker rmi streamlit-analyzer
```

### Отладка | Debugging

```bash
# Подключение к контейнеру | Connect to container
docker exec -it streamlit-app /bin/bash

# Просмотр логов в реальном времени | Real-time logs
docker logs -f streamlit-app
```

## Технические детали | Technical Details

- **Базовый образ | Base image:** python:3.11-slim
- **Порт приложения | App port:** 8501 (внутри контейнера | inside container)
- **Внешний порт | External port:** 8502
- **Пользователь | User:** app (для безопасности | for security)
- **Рабочая директория | Working directory:** /app

## Устранение неполадок | Troubleshooting

### Порт уже занят | Port already in use
```bash
# Использовать другой порт | Use different port
docker run -d -p 8503:8501 --name streamlit-app streamlit-analyzer
```

### Контейнер не запускается | Container won't start
```bash
# Проверить логи | Check logs
docker logs streamlit-app

# Запустить интерактивно для отладки | Run interactively for debugging
docker run -it --rm streamlit-analyzer /bin/bash
```