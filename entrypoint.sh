#!/bin/sh
set -e

tries=0
until python manage.py migrate --noinput; do
  tries=$((tries + 1))
  if [ "$tries" -ge 15 ]; then
    echo "Database not available, giving up."
    exit 1
  fi
  echo "Waiting for database ($tries/15)..."
  sleep 2
done

exec "$@"