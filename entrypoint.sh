#!/bin/sh

ENV_DIR=/env
GUNICORN_BIN=${ENV_DIR}/bin/gunicorn
PYTHON_BIN=${ENV_DIR}/bin/python
PIP_BIN=${ENV_DIR}/bin/pip
APP_MANAGE=/app/manage.py

if [ ! -d "$ENV_DIR" ]; then
    python3 -m venv $ENV_DIR
fi

if [ "$APP_ENV" == "development" ]; then
    $PIP_BIN install -Ur /app/requeriments/dev.txt
fi

for command in "$@"
do
    if [ "$command" == "runserver" ]; then
        if [ "$APP_ENV" == "development" ]; then
            $GUNICORN_BIN -b 0.0.0.0:8000 --reload --workers=1 --threads=2 --access-logfile /dev/stderr app.wsgi
        else
            $GUNICORN_BIN -b 0.0.0.0:8000 --workers=1 --threads=2 --access-logfile /dev/stderr  app.wsgi
        fi
    else
        $PYTHON_BIN $APP_MANAGE $1
    fi
done
