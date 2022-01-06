FROM python:3.9-slim-buster
ENV TZ="Canada/Eastern"
ENV PYTHONUNBUFFERED=1 DOCKER=1 DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install gunicorn[gevent]

RUN mkdir -p /src
COPY src /src/
RUN pip install -e /src

WORKDIR /src

EXPOSE 6001

CMD gunicorn --worker-class gevent --workers 4 --bind 0.0.0.0:6001 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
