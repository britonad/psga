#!/bin/sh
# NGINX start command.

# Build depends_on working alternative to docker-compose.
# Relation: Backend <- NGINX
# https://docs.docker.com/compose/startup-order/
while ! nc -z backend 8000; do
    echo "Waiting a few moments for the backend."
    sleep 3
done

nginx -g daemon off
