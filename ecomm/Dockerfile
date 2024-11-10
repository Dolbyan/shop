FROM python:3.9-slim
WORKDIR /ecomm
COPY ./ecomm /ecomm/
COPY ./requirements.txt /ecomm/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /ecomm/requirements.txt
ENV DJANGO_SETTINGS_MODULE=ecomm.settings
EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]