.PHONY: run
run:
	@CONFIG_PATH=config/dev.json python src/main.py

.PHONY: lint
lint:
	@flake8

.PHONY: test
test:
	@PYTHONPATH=./src python tests/run_tests.py
