FROM python:3.8-slim-buster

WORKDIR /chall/

COPY ./app .

RUN pip3 install -r requirements.txt


CMD ["python3","-m","flask","run","--host=0.0.0.0"]
