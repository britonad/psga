#!/bin/sh
# Backend Dockerfile start command.

# Run migrations for development but for the production, it's better to
# decouple this functionality to be performed manually by the DevOps team to
# avoid parallel migrations that lead to breakage and mental coupling.
python manage.py migrate

# Run gunicorn.
gunicorn -b 0.0.0.0 --workers 2 --log-level DEBUG --timeout 60 core.wsgi
