FROM node:17

RUN mkdir app
WORKDIR app

COPY . /app

CMD ["bash", ".docker/dev/start-typescript-watch.sh"]