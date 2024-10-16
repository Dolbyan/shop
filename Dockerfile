FROM python:3.9-slim
WORKDIR /app
COPY ./adminservice /app/adminservice
COPY kafka_consumer.py /app/
COPY requirements.txt .
RUN ls -la /app
RUN ls -la /app/adminservice
RUN cat /app/kafka_consumer.py
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/adminservice"
CMD ["python", "kafka_consumer.py"]
