FROM python:3.9-slim
WORKDIR /app
COPY ./ecomm /app/ecomm
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/ecomm/requirements.txt
ENV DJANGO_SETTINGS_MODULE=ecomm.settings
EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]