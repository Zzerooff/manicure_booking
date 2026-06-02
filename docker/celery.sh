#!/bin/bash


if [[ "${1}" == "celery" ]]; then
  cd /manicure_natali
  celery --app=app.tasks.celery:celery_app worker -l INFO

elif [[ "${1}" == "flower" ]]; then
  cd /manicure_natali
  celery --app=app.tasks.celery:celery_app flower
fi