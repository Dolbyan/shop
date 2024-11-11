FROM python:3.9-slim
WORKDIR /app/admin
COPY ./admin_app /app/admin/
COPY requirements.txt /app/admin/
RUN pip install -r requirements.txt
ENV PYTHONPATH="/app/admin:${PYTHONPATH}"
ENV DJANGO_SETTINGS_MODULE=eshop.settings
EXPOSE 8001  # zmieniony port
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]