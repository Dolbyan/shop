FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY admin_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY admin_app /app/admin_app
COPY admin_app/manage.py /app/manage.py
COPY admin_app/eshop /app/eshop

# Set environment variables
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=admin_app.eshop.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Use gunicorn with multiple workers
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn --workers 4 --threads 2 --bind 0.0.0.0:8000 admin_app.eshop.wsgi:application"]