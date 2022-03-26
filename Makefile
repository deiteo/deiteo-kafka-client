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
	poetry run wily build -n 10 -o cyclomatic,raw,maintainability,halstead

.PHONY: wily
wily:
	poetry run wily index
	poetry run wily rank --asc --threshold=50 wily-rank.txt | tee wily-rank.txt
	poetry run wily graph wily-target.txt -c mi -o res-main.html
	poetry run wily graph -c complexity -o wily-complex-path

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
