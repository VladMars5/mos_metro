#!/bin/bash

echo "Sleeping for 30 seconds…"
sleep 30

echo "Alembic migrations"
alembic upgrade head

cd src

python -u parser.py