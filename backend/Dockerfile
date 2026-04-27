    FROM python:3.11-slim

    WORKDIR /app

    # Устанавливаем системные зависимости (если понадобятся для сборки)
    # Для sqlite и базового python в slim-версии обычно ничего не нужно

    # Копируем список зависимостей
    COPY requirements.txt .

    # Устанавливаем зависимости
    # --no-cache-dir уменьшает размер образа, не сохраняя скачанные пакеты внутри
    RUN pip install --no-cache-dir -r requirements.txt

    # Копируем всё содержимое папки (main.py, mail_service.py и т.д.)
    COPY . .

    # Открываем порт 8000
    EXPOSE 8000

    # Запуск. Используем стандартную команду uvicorn
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
