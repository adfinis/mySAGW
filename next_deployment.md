# Manual steps for next deployment

## Fixed application template

Upload new template:

```bash
docker compose run --rm api poetry run ./manage.py upload_template -t mysagw/case/templates/application.docx
```

## Set env var in `.envs/.production/.caluma`

`DISABLE_INTROSPECTION=false`
