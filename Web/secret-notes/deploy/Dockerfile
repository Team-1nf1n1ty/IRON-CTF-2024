FROM python:slim-buster

WORKDIR /app/

COPY ./app .

RUN pip3 install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
