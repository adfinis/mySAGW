#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER caluma WITH PASSWORD '$CALUMA_DB_PASSWORD';
    CREATE DATABASE caluma OWNER caluma;
    GRANT CONNECT ON DATABASE caluma TO caluma;
    ALTER USER caluma CREATEDB;
EOSQL
