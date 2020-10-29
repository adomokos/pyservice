THIS_FILE := $(lastword $(MAKEFILE_LIST))

.DEFAULT_GOAL := help

run: ## Run the app
	poetry run my-script
.PHONY: run

lint: ## Lint the code
	poetry run flake8 pyservice spec
	poetry run mypy pyservice spec

spec: ## Run the specs
	poetry run mamba spec --format=documentation --enable-coverage
.PHONY: spec

coverage: ## Run the coverage report
	poetry run coverage report --fail-under=95
.PHONY: coverage

repl: ## Fire up the Repl
	poetry run python
.PHONY: repl

help: ## Prints this help message
	@grep -h -E '^[a-zA-Z0-9\._-]+:.*?## .*$$' $(MAKEFILE_LIST) |\
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help
