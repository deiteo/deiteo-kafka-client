export APP := deiteo/kafka-client
export TAG := 0.0.4

setup-environment: install-environment setup-wily install-linter clean-environment

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

.PHONY: setup-wily
setup-wily:
	poetry run wily clean --yes
	poetry run wily build src/ tests/ src/deiteo_kafka/producer -n 100 -o cyclomatic,raw,maintainability,halstead

.PHONY: wily-operators
wily-operators:
	poetry run wily index
	poetry run wily rank --asc --threshold=80
	poetry run wily report src/deiteo_kafka/log.py
	poetry run wily report src/deiteo_kafka/producer/deiteo_kafka_aio_producer.py

.PHONY: install-linter
install-linter:
	poetry run pre-commit clean
	poetry run pre-commit install

.PHONY: linter
linter:
	poetry run pre-commit run --all-files

.PHONY: run-container-linter
run-container-linter:
	docker run $(APP):$(TAG) make --directory app/ linter

.PHONY: build-container-image
build-container-image:
	docker build -t $(APP):$(TAG) -f tools/docker/Dockerfile .

.PHONY: get-container-info-environment
get-container-info-environment:
	docker run $(APP):$(TAG) make --directory app/ info-environment

.PHONY: run-container-tests
run-container-tests:
	docker run $(APP):$(TAG) make --directory app/ test type=$(type)
