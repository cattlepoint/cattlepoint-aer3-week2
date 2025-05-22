#!/bin/sh
set -e

echo "⏳ waiting for $MYSQL_HOST …"
until mariadb -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" \
              -e "SELECT 1" "$MYSQL_DATABASE" >/dev/null 2>&1; do
  sleep 2
done

echo "🚀 seeding $MYSQL_DATABASE"
mariadb -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" \
        "$MYSQL_DATABASE" < /seed.sql
echo "✅ done"
