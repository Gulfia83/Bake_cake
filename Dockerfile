FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=Bake_cake.settings
ENV PYTHONUNBUFFERED=1

# RUN python manage.py migrate

RUN [ -f /app/start.sh ] && chmod +x /app/start.sh || echo "File /app/start.sh not found"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
