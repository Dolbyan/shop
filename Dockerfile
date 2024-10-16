FROM python:3.9-slim
WORKDIR /app
COPY kafka_consumer.py /app/
COPY requirements.txt /app/
COPY adminservice /app/adminservice
COPY ecomm /app/ecomm
RUN pip install -r requirements.txt
CMD ["python", "kafka_consumer.py"]