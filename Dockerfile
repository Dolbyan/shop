FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/consumer
COPY ./admin_app /app/consumer/admin_app
COPY ./ecomm /app/consumer/ecomm
COPY kafka_consumer.py kafka_consumer_settings.py ./

ENV PYTHONPATH="/app/consumer:${PYTHONPATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "kafka_consumer.py"]
