FROM python:3.9-slim
WORKDIR /app

# Instalacja zależności
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    postgresql-client

# Skrypt oczekujący na bazę
COPY ./wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

# Kopiowanie kodu i instalacja zależności Pythona
COPY ecomm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Komenda startowa
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "ecomm.ecomm.wsgi:application"]