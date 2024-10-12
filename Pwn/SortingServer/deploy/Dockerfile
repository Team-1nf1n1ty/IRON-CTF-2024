FROM ubuntu:22.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user


COPY flag.txt /home/user/
COPY sortingserver /home/user/
COPY libc.so.6 /home/user/
COPY ld-linux-x86-64.so.2 /home/user/

RUN chmod +x /home/user/sortingserver
RUN chmod +x /home/user/libc.so.6
RUN chmod +x /home/user/ld-linux-x86-64.so.2

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot
COPY nsjail.cfg /home/user/

EXPOSE 1337

CMD kctf_setup && \
    kctf_drop_privs \
   kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/sortingserver
