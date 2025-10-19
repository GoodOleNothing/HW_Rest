# Используем официальный образ Python
FROM python:3.11-slim

# Создаем директорию проекта
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Django port
EXPOSE 8000

#  Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]