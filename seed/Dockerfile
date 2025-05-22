FROM alpine:3.21

RUN apk add --no-cache mariadb-client

ENV MYSQL_HOST=host.containers.internal \
    MYSQL_DATABASE=appdb \
    MYSQL_USER=appuser \
    MYSQL_PASSWORD=apppassword

COPY seed.sql /seed.sql
COPY seed.sh  /seed.sh
RUN chmod +x /seed.sh

CMD ["/seed.sh"]
