FROM python:3.8.6

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY ./app /opt/app

WORKDIR /opt

ENTRYPOINT uvicorn --factory app.asgi:factory --host 0.0.0.0 --port 8000