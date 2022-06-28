#!/bin/bash

make collectstatic
make migrate
gunicorn config.wsgi --workers=$GUNICORN_WORKERS --bind=0.0.0.0:8000 --chdir=/opt/web
