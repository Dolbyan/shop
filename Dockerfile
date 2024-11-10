FROM python:3.9-slim
WORKDIR /lesson3

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./admin_app /lesson3/admin_app
COPY ./ecomm /lesson3/ecomm
COPY kafka_consumer.py /lesson3/
COPY kafka_consumer_settings.py /lesson3/


RUN ls -R /lesson3
RUN ls -la /lesson3
RUN ls -la /lesson3/admin_app
RUN cat /lesson3/kafka_consumer.py

ENV PYTHONPATH="/lesson3"
CMD ["python", "kafka_consumer.py"]
