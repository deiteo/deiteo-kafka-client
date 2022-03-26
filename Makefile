export APP := deiteo/kafka-client
export TAG := 0.0.1-alpha.0

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
	poetry run wily build src/ tests/ -n 10 -o cyclomatic,raw,maintainability,halstead
	poetry run wily index

.PHONY: wily-operators-src
wily-operators-src:
	poetry run wily rank src/ --asc --threshold=80
	poetry run wily report src/deiteo_kafka/log.py
	poetry run wily report src/deiteo_kafka/producer/deiteo_kafka_aio_producer.py

.PHONY: wily-operators-tests
wily-operators-tests:
	poetry run wily rank tests/ --asc --threshold=80
	poetry run wily report tests/conftest.py
	poetry run wily report tests/unit/src/deiteo_kafka/producer/test_deiteo_kafka_aio_producer.py

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
