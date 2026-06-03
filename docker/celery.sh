#!/bin/bash

if [ -z "${1}" ]; then
  echo "Usage: $0 [celery|flower]"
  exit 1
fi

if [[ "${1}" == "celery" ]]; then
  echo "Starting Celery worker..."
  celery --app=app.tasks.celery:celery_app worker -l INFO

elif [[ "${1}" == "flower" ]]; then
  echo "Starting Flower dashboard..."
  celery --app=app.tasks.celery:celery_app flower
fi