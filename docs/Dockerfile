FROM node:20 AS builder

WORKDIR /app
COPY . .

RUN npm install

RUN npx tsc

FROM node:20 AS production

WORKDIR /app

COPY package*.json ./
RUN npm install --only=production

COPY --from=builder /app/dist ./dist
COPY ./docs ./docs

ENV NODE_ENV=production
ENV APP_PORT=5013
EXPOSE ${APP_PORT}

CMD ["node", "dist/main.js"]
