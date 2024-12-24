.PHONY: clean clean-pyc clean-test clean-build help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

VENV = .venv
TEST_VENV = .venv.test
PYTHON = python3
PIP = pip3
TEST_VENV_BIN = $(TEST_VENV)/bin
VENV_BIN = $(VENV)/bin
PID_FILE = dell_unisphere_mock_api.pid

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts
	rm -rf $(VENV)
	rm -rf $(TEST_VENV)
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .venv*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f $(PID_FILE)

clean-build: ## remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .tox/
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache
	rm -rf .mypy_cache

venv: ## create virtual environment
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -e ".[test,dev]"
	$(VENV_BIN)/pre-commit install

test-venv: ## create test virtual environment
	test -d $(TEST_VENV) || $(PYTHON) -m venv $(TEST_VENV)
	$(TEST_VENV_BIN)/pip install --upgrade pip
	$(TEST_VENV_BIN)/pip install -e ".[test]"

test: test-venv ## run tests with coverage reporting
	$(TEST_VENV_BIN)/pytest -v tests/ --cov=dell_unisphere_mock_api --cov-report=term-missing --cov-report=xml:coverage.xml

lint: venv ## run all linters
	$(VENV_BIN)/pre-commit run --all-files

format: venv ## format code with black and isort
	$(VENV_BIN)/black .
	$(VENV_BIN)/isort .

typecheck: venv ## run mypy type checking
	$(VENV_BIN)/mypy dell_unisphere_mock_api tests

security: venv ## run security checks
	$(VENV_BIN)/bandit -r dell_unisphere_mock_api

build: clean ## build source and wheel package
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

release: dist ## package and upload a release
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload dist/*

run: venv ## run development server
	$(VENV_BIN)/python -m dell_unisphere_mock_api
