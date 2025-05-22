# Use the current GA “latest” MariaDB image (11.4.6 as of May 22 2025)
FROM mariadb:latest

# Set initial credentials and database (override with -e at run-time if needed)
ENV MYSQL_ROOT_PASSWORD=rootpassword \
    MYSQL_DATABASE=appdb \
    MYSQL_USER=appuser \
    MYSQL_PASSWORD=apppassword

# Make the standard MariaDB port available for docker run -p/-P
EXPOSE 3306
