FROM python:3.9-slim
WORKDIR /app
COPY ./admin_app /app/
RUN pip install -r requirements.txt
ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV DJANGO_SETTINGS_MODULE=admin_app.eshop.settings
EXPOSE 8000
CMD ["python", "addmin_app/manage.py", "runserver", "0.0.0.0:8000"]