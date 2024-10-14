FROM python:3.9-slim
WORKDIR /app
COPY kafka_consumer.py /app/
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "kafka_consumer.py"]