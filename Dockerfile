FROM python:3.9

WORKDIR /app


COPY kafka_consumer.py /app/
COPY kafka_consumer_settings.py /app/
COPY requirements.txt /app/

COPY admin_app /app/admin_app/
COPY ecomm /app/ecomm/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app:/app/admin_app:/app/ecomm

CMD ["python", "kafka_consumer.py"]