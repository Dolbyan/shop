FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/ecomm
COPY ./ecomm .
ENV PYTHONPATH=/app/ecomm
ENV DJANGO_SETTINGS_MODULE=ecomm.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8001
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "ecomm.wsgi:application"]