FROM docker.io/python:3.10-alpine

COPY flask/ /app
COPY requirements.txt /app/requirements.txt

RUN mkdir /Podcasts && \
    cd /app && \
    pip install -r requirements.txt && \
    mkdir -p /app/data

WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--worker-class", "gevent", "--log-level", "info", "wsgi:app"]
