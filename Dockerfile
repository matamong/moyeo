FROM tiangolo/uvicorn-gunicorn:python3.11-slim

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

WORKDIR /src

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY ./start-reload.sh /src/start-reload.sh
RUN chmod +x start-reload.sh

COPY ./app/prestart.sh /src/app/prestart.sh
RUN chmod +x app/prestart.sh

COPY . /src


EXPOSE 8000

CMD ["/start-reload.sh"]


