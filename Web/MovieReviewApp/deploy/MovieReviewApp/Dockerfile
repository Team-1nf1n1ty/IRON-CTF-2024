FROM python:3.10-slim 
WORKDIR /app
COPY movies /app/movies
COPY git /app/.git

CMD [ "python", "-m", "http.server" ,"8080" ]