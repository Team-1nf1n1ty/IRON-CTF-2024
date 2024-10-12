FROM php:8.2-apache

WORKDIR /var/www/html

COPY chall .
COPY source /


ENV FLAG ironCTF{D353r1411Z4710N_4T_1T5_B35T}

EXPOSE 80

CMD ["php","-S","0.0.0.0:80"]
