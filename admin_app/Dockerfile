FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/admin
COPY . .
ENV PYTHONPATH=/app/admin_app
ENV DJANGO_SETTINGS_MODULE=admin_app.eshop.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "admin_app.eshop.wsgi:application"]