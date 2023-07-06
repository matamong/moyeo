FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

ENV PYTHONPATH=/app


CMD ["/app/start-reload.sh"]

