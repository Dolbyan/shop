FROM python:3.9-slim
WORKDIR /app
COPY kafka_consumer.py /app/
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "kafka_consumer.py"]