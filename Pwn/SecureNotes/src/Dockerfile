FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libc6-dev

COPY SecureNotes.c /usr/src/SecureNotes.c

WORKDIR /usr/src

RUN gcc SecureNotes.c -o SecureNotes

CMD ["./SecureNotes"]
