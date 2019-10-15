#!/bin/sh
# Backend Dockerfile start command.

# Build depends_on working alternative to docker-compose.
# Relation: PostgreSQL <- Backend
# https://docs.docker.com/compose/startup-order/
while ! nc -z postgresql 5432; do
    echo "Waiting a few moments for the postgres database."
    sleep 3
done

# Run migrations for development but for the production, it's better to
# decouple this functionality to be performed manually by the DevOps team to
# avoid parallel migrations that lead to breakage and mental coupling.
python manage.py migrate

# Run gunicorn.
gunicorn -b 0.0.0.0 --workers 2 --log-level DEBUG --timeout 60 core.wsgi
