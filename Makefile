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
	@docker compose run --rm api pytest --no-cov-on-fail --cov -vv

.PHONY: api-lint
api-lint: ## Lint the backend
	@docker compose run --rm api sh -c "ruff format --diff . && ruff check ."

.PHONY: api-shell
api-shell: ## Shell into the backend
	@docker compose run --rm api sh

.PHONY: api-shell_plus
api-shell_plus: ## Run shell_plus
	@docker compose run --rm api ./manage.py shell_plus

.PHONY: api-dev-server
api-dev-server: ## Start backend dev server
	@docker compose stop api
	@docker compose run --user root --use-aliases --service-ports api sh -c "poetry run pip install pdbpp && poetry run python manage.py runserver 0.0.0.0:8000"

.PHONY: makemigrations
makemigrations: ## Make django migrations
	@docker compose run --rm api ./manage.py makemigrations

.PHONY: migrate
migrate: ## Migrate django
	@docker compose run --rm api ./manage.py migrate

.PHONY: dbshell
dbshell: ## Start a psql shell
	@docker compose exec db psql -Umysagw

.PHONY: caluma-test
caluma-test: ## test caluma config and extensions
	@docker compose exec -T caluma poetry run python manage.py check
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
	@docker compose run --rm ember yarn lint

.PHONY: ember-lint-fix
ember-lint-fix: ## lint and fix the frontend
	@docker compose run --rm ember yarn lint:js --fix

.PHONY: ember-test
ember-test: ## test the frontend
	@docker compose run --rm ember yarn test:ember

.PHONY: keycloak-import-config
keycloak-import-config: ## import the Keycloak config for local development
	@docker compose exec keycloak /opt/keycloak/bin/kc.sh import --override true --file /opt/keycloak/data/import/test-config.json

.PHONY: keycloak-export-config
keycloak-export-config: ## export the Keycloak config
	@docker compose run --rm keycloak export --file /opt/keycloak/data/import/test-config.json
