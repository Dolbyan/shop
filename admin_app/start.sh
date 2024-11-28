#!/bin/bash

# Czekaj na dostępność bazy danych
until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing migrations"

# Wykonaj migracje i uruchom aplikację
python manage.py makemigrations
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 admin_app.eshop.wsgi:application
