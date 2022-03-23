export APP := deiteo/kafka-client
export TAG := 0.0.1

setup-environment: clean-environment install-environment install-linter

.PHONY: clean-environment
clean-environment:
	rm -rf build dist .eggs *.egg-info
	rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	find . -type f -name "*.py[co]" -exec rm -rf {} +

.PHONY: install-environment
install-environment:
	poetry env use 3.8
	poetry install

.PHONY: info-environment
info-environment:
	poetry env info
	poetry show --tree

.PHONY: test
test:
	poetry run python -m pytest tests/$(type)/ --cov-config=tests/$(type)/.coveragerc --cov=. --quiet $(test_argument)

.PHONY: update-environment
update-environment:
	poetry update

.PHONY: install-linter
install-linter:
	poetry run pre-commit clean
	poetry run pre-commit install

.PHONY: linter
linter:
	poetry run pre-commit run --all-files
