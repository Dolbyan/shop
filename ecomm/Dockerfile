FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=ecomm.ecomm.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8001
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "ecomm.ecomm.wsgi:application"]