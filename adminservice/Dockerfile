FROM python:3.9-slim
WORKDIR /app
COPY ./ /app/
RUN pip install -r requirements.txt
ENV PYTHONPATH=/app/adminservice:/app/ecomm
ENV DJANGO_SETTINGS_MODULE=adminservice.eshop.settings
EXPOSE 8000
CMD ["python", "/app/adminservice/manage.py", "runserver", "0.0.0.0:8000"]