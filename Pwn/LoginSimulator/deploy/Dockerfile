FROM pwn.red/jail
COPY --from=ubuntu / /srv
COPY flag.txt /srv/app/
COPY .glibc /srv/app/.glibc
COPY login /srv/app/run
