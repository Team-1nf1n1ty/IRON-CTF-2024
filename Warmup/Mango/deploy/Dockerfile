FROM node:lts-alpine

WORKDIR /app

COPY app/package*.json ./

RUN npm ci

COPY app .

EXPOSE 3000

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
