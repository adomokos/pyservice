THIS_FILE := $(lastword $(MAKEFILE_LIST))

.DEFAULT_GOAL := help

run: ## Run the app
	poetry run my-script
.PHONY: run

lint: ## Lints the code
	poetry run flake8 pyservice test
	poetry run mypy pyservice test
	poetry run black . --check

test: ## Run the tests
	poetry run pytest
.PHONY: test

fmt: ## Formats the code
	poetry run black .

coverage: ## Run the coverage report
	poetry run pytest --cov-report term --cov=pyservice test/
	poetry run coverage-badge -o coverage.svg -f
.PHONY: coverage

repl: ## Fire up the Repl
	poetry run python
.PHONY: repl

help: ## Prints this help message
	@grep -h -E '^[a-zA-Z0-9\._-]+:.*?## .*$$' $(MAKEFILE_LIST) |\
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help
