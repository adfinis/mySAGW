.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the development server
	@docker-compose build --pull

.PHONY: start
start: ## Start the development server
	@docker-compose up -d --build

.PHONY: api-test
api-test: ## Test the backend
	@docker-compose run api pytest --no-cov-on-fail --cov --create-db -vv

.PHONY: api-lint
api-lint: ## Lint the backend
	@docker-compose run api sh -c "black --check . && flake8"

.PHONY: api-bash
api-bash: ## Shell into the backend
	@docker-compose run api bash

.PHONY: api-shell_plus
api-shell_plus: ## Run shell_plus
	@docker-compose run api python ./manage.py shell_plus

.PHONY: makemigrations
makemigrations: ## Make django migrations
	@docker-compose run api python ./manage.py makemigrations

.PHONY: migrate
migrate: ## Migrate django
	@docker-compose run api python ./manage.py migrate

.PHONY: dbshell
dbshell: ## Start a psql shell
	@docker-compose exec db psql -Umysagw

.PHONY: caluma-test
caluma-test: ## test caluma config and extensions
	@docker-compose exec -T caluma python manage.py check
	@docker-compose exec -T caluma ./caluma/ci/test.sh

.PHONY: caluma-lint
caluma-lint: ## lint caluma extensions
	@cd ./caluma && black --check .
	@cd ./caluma && flake8
