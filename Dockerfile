FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY src/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY src/app/ .

# Создание директории для данных
RUN mkdir -p /app/database /app/logs

VOLUME ["/app/database", "/app/logs"]

CMD ["python", "main.py"]
