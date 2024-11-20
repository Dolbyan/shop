FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./admin_app /app/admin_app
COPY manage.py /app/
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=admin_app.eshop.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 admin_app.eshop.wsgi:application"]