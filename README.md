# mySAGW

[![Build Status](https://github.com/adfinis/mySAGW/workflows/Tests/badge.svg)](https://github.com/adfinis/mySAGW/actions?query=workflow%3ATests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/adfinis/mySAGW/blob/master/api/setup.cfg#L53)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![License: GPL-3.0-or-later](https://img.shields.io/github/license/adfinis-sygroup/mySAGW)](https://spdx.org/licenses/GPL-3.0-or-later.html)

Application management for SAGW

## Getting started

### Installation (dev)

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/adfinis/mysagw/main/docker-compose.yml) and run the following command:

```bash
echo "UID=$(id -u)" > .env
touch ./caluma/.env
docker-compose up -d
```

Wait for the database migrations to complete for the API and Caluma.

Load the config data into Caluma:

```bash
make caluma-loadconfig
```

Import the Keycloak config:

```bash
docker-compose exec keycloak /opt/keycloak/bin/kc.sh import --override true --file /opt/keycloak/data/import/test-config.json
```

Add `mysagw.local` to `/etc/hosts`:

```bash
echo "127.0.0.1 mysagw.local" | sudo tee -a /etc/hosts
```

You can now access the application under the following URIs:

 - https://mysagw.local/ --> frontend
 - https://mysagw.local/auth/ --> keycloak
 - https://mysagw.local/api/ --> backend
 - https://mysagw.local/graphql/ --> caluma
 - https://mysagw.local:8025 --> mailhog

The default users are:

| Username          | Password | Used for       |
|-------------------|----------|----------------|
| admin             | keycloak | keycloak admin |
| admin@example.com | mysagw   | apps           |
| staff@example.com | mysagw   | apps           |
| user@example.com  | mysagw   | apps           |

### Configuration

mySAGW is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://django-environ.readthedocs.io/en/latest/types.html).


### Deployment

```bash
cp -r ./.envs/.production.example ./.envs/.production
```

Then edit the files under `./.envs/.production/` to your needs.

For the staging environment, copy to `./.envs/.staging/`.

```bash
echo -e "UID=$(id -u)\nCOMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml" > .env
# on staging environments:
# echo -e "UID=$(id -u)\nCOMPOSE_FILE=docker-compose.yml:docker-compose.staging.yml" > .env
# Also in .env file, set OIDC_HOST variable
docker compose up -d
# Wait for the database migrations to complete for the API and Caluma.
make caluma-loadconfig
# upload the templates to DMS
docker compose run --rm api python manage.py upload_template -t identity-labels.docx
docker compose run --rm api python manage.py upload_template -t accounting-cover.docx
docker compose run --rm api python manage.py upload_template -t acknowledgement-de.docx
docker compose run --rm api python manage.py upload_template -t acknowledgement-fr.docx
docker compose run --rm api python manage.py upload_template -t acknowledgement-en.docx
docker compose run --rm api python manage.py upload_template -t credit-approval-de.docx
docker compose run --rm api python manage.py upload_template -t credit-approval-fr.docx
docker compose run --rm api python manage.py upload_template -t credit-approval-en.docx
docker compose run --rm api python manage.py upload_template -t application.docx
```

## Contributing

Look at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.
