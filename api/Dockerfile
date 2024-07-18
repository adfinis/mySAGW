FROM python:3.9

# needs to be set for users with manually set UID
ENV HOME=/home/mysagw

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE mysagw.settings
ENV APP_HOME=/app

RUN mkdir -p /app \
&& useradd -u 901 -r mysagw --create-home \
# all project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
&& chown -R mysagw:root /home/mysagw \
&& chmod -R 770 /home/mysagw \
&& apt-get update && apt-get install -y --no-install-recommends \
    wait-for-it \
    # needed for psycopg2
    libpq-dev \
&& pip install -U poetry

USER mysagw

WORKDIR $APP_HOME

ARG INSTALL_DEV_DEPENDENCIES=false
COPY pyproject.toml poetry.lock $APP_HOME/
RUN if [ "$INSTALL_DEV_DEPENDENCIES" = "true" ]; then poetry install; else poetry install --without dev; fi

COPY . $APP_HOME

EXPOSE 8000

CMD [\
    "/bin/sh", "-c", \
    "wait-for-it $DATABASE_HOST:${DATABASE_PORT:-5432} -- \
    poetry run ./manage.py migrate && \
    exec poetry run gunicorn --workers 10 --access-logfile - --limit-request-line 16384 --bind 0.0.0.0:8000 mysagw.wsgi" \
]
