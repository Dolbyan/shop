FROM python:3.9-slim
WORKDIR /app
COPY ./adminservice /app/
RUN pip install -r adminservice/requirements.txt
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=adminservice.eshop.settings
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]