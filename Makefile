.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the development server
	@docker compose build --pull

.PHONY: start
start: ## Start the development server
	@docker compose up -d --build

.PHONY: api-test
api-test: ## Test the backend
	@docker compose run --rm api poetry run pytest --no-cov-on-fail --cov -vv

.PHONY: api-lint
api-lint: ## Lint the backend
	@docker compose run --rm api sh -c "poetry run ruff format --diff . && poetry run ruff check ."

.PHONY: api-bash
api-bash: ## Shell into the backend
	@docker compose run --rm api bash

.PHONY: api-shell_plus
api-shell_plus: ## Run shell_plus
	@docker compose run --rm api poetry run ./manage.py shell_plus

.PHONY: api-dev-server
api-dev-server: ## Start backend dev server
	@docker compose stop api
	@docker compose run --user root --use-aliases --service-ports api bash -c 'pip install pdbpp && poetry run ./manage.py runserver 0.0.0.0:8000'

.PHONY: makemigrations
makemigrations: ## Make django migrations
	@docker compose run --rm api poetry run ./manage.py makemigrations

.PHONY: migrate
migrate: ## Migrate django
	@docker compose run --rm api poetry run ./manage.py migrate

.PHONY: dbshell
dbshell: ## Start a psql shell
	@docker compose exec db psql -Umysagw

.PHONY: caluma-test
caluma-test: ## test caluma config and extensions
	@docker compose exec -T caluma poetry run python manage.py check
	@docker compose exec -T -u root caluma poetry install --no-root
	@docker compose exec -T caluma ./caluma/ci/test.sh

.PHONY: caluma-lint
caluma-lint: ## lint caluma extensions
	@cd ./api && poetry run bash -c "cd ../caluma && ruff format --diff ."
	@cd ./api && poetry run ruff check ../caluma

.PHONY: caluma-load-workflow
caluma-load-workflow: ## Load workflow config from JSON
	@docker compose exec caluma poetry run python manage.py loaddata caluma/data/workflow-config.json

.PHONY: caluma-load-form
caluma-load-form: ## Load form config from JSON
	@docker compose exec caluma poetry run python manage.py loaddata caluma/data/form-config.json

.PHONY: caluma-loadconfig
caluma-loadconfig: caluma-load-form caluma-load-workflow ## Load workflow and form config from JSON

.PHONY: caluma-dump-forms
caluma-dump-forms: ## dump Caluma form models including default answers
	@docker compose run --rm caluma poetry run python manage.py dumpdata --indent 4 \
	caluma_form.Form caluma_form.FormQuestion caluma_form.Question \
	caluma_form.QuestionOption caluma_form.Option caluma_form.Answer \
	caluma_analytics.AnalyticsTable caluma_analytics.AnalyticsField | sed -e \
	's/\r$$//' | jq '.[] | select(.fields.document == null)' | jq -s '.' --indent 4

.PHONY: caluma-dump-workflow
caluma-dump-workflow: ## dump Caluma workflow models
	@docker compose run --rm caluma poetry run python manage.py dumpdata --indent 4 \
	caluma_workflow.Task caluma_workflow.Workflow caluma_workflow.Flow \
	caluma_workflow.TaskFlow | sed -e 's/\r$$//'

.PHONY: caluma-flush
caluma-flush: ## flush the Caluma database
	@docker compose exec caluma poetry run python manage.py flush --no-input

.PHONY: caluma-foreground
caluma-foreground: ## run caluma in foreground with dev server for debugging
	@docker compose stop caluma
	@docker compose run --rm -u root --use-aliases --service-ports caluma bash -c \
	'poetry run pip install pdbpp && poetry run python ./manage.py runserver 0.0.0.0:8000'

.PHONY: ember-lint
ember-lint: ## lint the frontend
	@docker compose run --rm ember pnpm run lint

.PHONY: ember-lint-fix
ember-lint-fix: ## lint and fix the frontend
	@docker compose run --rm ember pnpm run lint:js --fix

.PHONY: ember-test
ember-test: ## test the frontend
	@docker compose run --rm ember pnpm run test:ember
