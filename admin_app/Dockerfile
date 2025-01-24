FROM python:3.9-slim
WORKDIR /app

# Instalacja zależności
RUN apt-get update && apt-get install -y \ netcat \ postgresql-client
# Skrypt oczekujący na bazę
COPY ./wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

# Kopiowanie kodu i instalacja zależności Pythona
COPY admin_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY admin_app /app/admin_app

# Komenda startowa
CMD ["sh", "-c", "./wait-for-postgres.sh postgres-service:5432 -- python manage.py makemigrations && python manage.py migrate && gunicorn --workers 4 --threads 2 --bind 0.0.0.0:8000 admin_app.eshop.wsgi:application"]