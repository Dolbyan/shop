FROM python:3.9-slim
WORKDIR /app

# Instaluj potrzebne pakiety
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY admin_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY admin_app /app/admin_app
COPY admin_app/manage.py /app/manage.py
COPY admin_app/eshop /app/eshop
COPY admin_app/eshop/settings.py /app/eshop/settings.py

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=admin_app.eshop.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dodaj skrypt startowy
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]