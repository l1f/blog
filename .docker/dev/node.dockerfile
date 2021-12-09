FROM node:17

RUN mkdir app
WORKDIR app

COPY . /app

CMD ["npm", "./.docker/dev/start-nodemon.sh"]