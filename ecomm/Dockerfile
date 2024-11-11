FROM python:3.9-slim
WORKDIR /app/ecomm
COPY ./ecomm /app/ecomm/
COPY requirements.txt /app/ecomm/
RUN pip install -r requirements.txt
ENV PYTHONPATH="/app/ecomm:${PYTHONPATH}"
ENV DJANGO_SETTINGS_MODULE=ecomm.settings
EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]