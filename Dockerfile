FROM python:3.9-slim
WORKDIR /app
COPY ./adminservice /app/adminservice
COPY kafka_consumer.py /app/
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN ls -la /app
RUN cat /app/kafka_consumer.py
ENV PYTHONPATH="${PYTHONPATH}:/app"
CMD ["python", "kafka_consumer.py"]
