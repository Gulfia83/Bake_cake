#!/bin/bash

# Запуск Django в фоновом режиме
python manage.py runserver 0.0.0.0:8000 &

# Запуск Telegram бота
python bot.py
