FROM python:3.9-slim
WORKDIR /lesson3
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./adminservice /lesson3/adminservice
COPY ./ecomm /lesson3/ecomm
COPY kafka_consumer.py /lesson3/

RUN ls -R /app
RUN ls -R /lesson3
RUN ls -la /lesson3
RUN ls -la /lesson3/adminservice
RUN cat /lesson3/kafka_consumer.py
ENV PYTHONPATH="/lesson3"
CMD ["python", "kafka_consumer.py"]
