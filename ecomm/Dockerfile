FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY ecomm/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ecomm/ /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "ecomm.wsgi:application"]