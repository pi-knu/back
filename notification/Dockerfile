FROM node:20

WORKDIR /app
COPY . .

RUN npm install

ENV APP_PORT=5012
EXPOSE ${APP_PORT}

CMD ["npm", "run", "start:dev"]
