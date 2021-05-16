FROM alpine:3.13

WORKDIR /app
COPY . /app

RUN apk add --update python3 python3-dev postgresql-dev build-base py3-virtualenv && \
    python3 -m venv /env && \
    /env/bin/pip install wheel && \
    /env/bin/pip install -Ur /app/requeriments/dev.txt

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["migrate", "runserver"]