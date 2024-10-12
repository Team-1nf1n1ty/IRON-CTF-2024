FROM python:3.9.7 as chroot


RUN mkdir -p /home/user

COPY ./app /home/user

WORKDIR /home/user

RUN mv flag.sh /usr/local/bin/flag

RUN pip install --no-cache-dir -r requirements.txt



FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f
COPY --from=chroot / /chroot
COPY nsjail.cfg /home/user/
COPY run.sh /chroot/home/user/
RUN chmod +x /chroot/home/user/run.sh
RUN chmod +x /chroot/usr/local/bin/flag

CMD kctf_setup && \
    kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /home/user/run.sh
