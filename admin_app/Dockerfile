FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY . /app
COPY admin_app/requirements.txt /app/admin_app/

RUN pip install --no-cache-dir -r /app/admin_app/requirements.txt


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "eshop.wsgi:application"]