# Явно указываем Python 3.11 (стабильная версия с колёсами для всех зависимостей)
FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Открываем порт (Render сам передаст $PORT)
EXPOSE 10000

# Команда запуска (uvicorn через gunicorn для продакшена)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]