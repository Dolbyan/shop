FROM python:3.9-slim
WORKDIR /app
COPY ./adminservice /app/adminservice
COPY ./ecomm /app/ecomm
COPY kafka_consumer.py /app/
COPY requirements.txt .
RUN ls -la /app
RUN ls -la /app/adminservice
RUN cat /app/kafka_consumer.py
ENV PYTHONPATH="/app"
CMD ["python", "kafka_consumer.py"]
