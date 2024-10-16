FROM python:3.9-slim
WORKDIR /app
COPY kafka_consumer.py /app/
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH="${PYTHONPATH}:/app/adminservice/eshop:/app/ecomm"
CMD ["python", "kafka_consumer.py"]