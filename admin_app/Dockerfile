FROM python:3.9-slim
WORKDIR /app


RUN apt-get update && apt-get install -y \
     netcat-traditional \
     postgresql-client

COPY ./wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

# Kopiowanie kodu i instalacja zależności Pythona
COPY admin_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY admin_app /app/admin_app

# Komenda startowa
CMD ["sh", "-c", "./wait-for-postgres.sh postgres-admin-service:5432 -- python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 admin_app.eshop.wsgi:application"]