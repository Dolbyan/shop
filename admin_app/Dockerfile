FROM python:3.9-slim
WORKDIR /app

COPY . .

COPY admin_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Komenda startowa
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "eshop.wsgi:application"]