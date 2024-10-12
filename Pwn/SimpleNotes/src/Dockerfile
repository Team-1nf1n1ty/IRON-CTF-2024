FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libc6-dev

COPY SimpleNotes.c /usr/src/SimpleNotes.c

WORKDIR /usr/src

RUN gcc SimpleNotes.c -o SimpleNotes

CMD ["./SimpleNotes"]
