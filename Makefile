# RUN with ENV variable set
.PHONY: run
run:
	@CONFIG_PATH=config/dev.json python src/main.py

# TEST
.PHONY: test
test:
	@PYTHONPATH=./src python tests/run_tests.py

# BUILD code transformations
.PHONY: black
black:
	@black ./src ./tests

.PHONY: isort
isort:
	@isort ./src ./tests

.PHONY: build
build: black isort

# CHECK linting and formatting
.PHONY: lint
lint:
	@flake8

.PHONY: mypy
mypy:
	@mypy .

.PHONY: black-check
black-check:
	@black --check ./src ./tests

.PHONY: isort-check
isort-check:
	@isort --check-only ./src ./tests

.PHONY: check
check: lint mypy black-check isort-check