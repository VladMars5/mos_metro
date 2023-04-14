#!/bin/bash

echo "Sleeping for 30 seconds…"
sleep 15

echo "Alembic migrations"
alembic upgrade head

cd src

gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000