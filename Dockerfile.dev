FROM python:3.10.0-alpine3.14

ENV FLASK_APP=managed.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_ENV="docker"


RUN apk add build-base

RUN mkdir app
WORKDIR app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
