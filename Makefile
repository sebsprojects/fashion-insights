.PHONY: run
run:
	@CONFIG_PATH=config/dev.json python src/main.py

.PHONY: test
test:
	@PYTHONPATH=./src python tests/run_tests.py
