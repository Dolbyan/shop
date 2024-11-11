FROM python:3.9-slim
WORKDIR /admin_app
COPY ./admin_app /admin_app/
COPY ./requirements.txt /admin_app/requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH="/admin_app:${PYTHONPATH}"
ENV DJANGO_SETTINGS_MODULE=eshop.settings
EXPOSE 8000
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
