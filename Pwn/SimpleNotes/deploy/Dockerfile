FROM pwn.red/jail
COPY --from=ubuntu / /srv
COPY flag.txt /srv/app/
COPY libc.so.6 /srv/app/
COPY ld-2.27.so /srv/app/
ENV JAIL_TIME=120
COPY SimpleNotes /srv/app/run
