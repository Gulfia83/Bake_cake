# Используем официальный образ Python в качестве базового
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

RUN apt-get update && apt-get install -y nano

# Устанавливаем зависимости проекта
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Устанавливаем переменные окружения для Django
ENV DJANGO_SETTINGS_MODULE=Bake_cake.settings
ENV PYTHONUNBUFFERED=1

# Применяем миграции базы данных
RUN python manage.py migrate
# Даем права на выполнение скрипта
RUN chmod +x /app/start.sh
# Удаляем лишние команды
# CMD ["/app/start.sh"]

# Команда для запуска приложения может быть задана в docker-compose.yml
