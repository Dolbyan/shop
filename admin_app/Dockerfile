FROM python:3.9-slim
WORKDIR /app
COPY ./admin_app /app/
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV DJANGO_SETTINGS_MODULE=eshop.settings
EXPOSE 8000
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
