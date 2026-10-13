#!/bin/sh
set -eu
echo "Waiting for PostgreSQL..."
python - <<'PY'
import os, time, psycopg
for attempt in range(60):
    try:
        with psycopg.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            connect_timeout=2,
        ):
            print("PostgreSQL is ready.")
            break
    except Exception as exc:
        if attempt == 59:
            raise SystemExit(f"PostgreSQL not ready: {exc}")
        time.sleep(2)
PY
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile - --error-logfile -
