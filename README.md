# Deiteo Kafka Client

## Requirement

## Setup

* ^python3.8
* poetry 1.1.13
* make (GNU Make 3.81)

```bash
make setup-environment
```

Update package
```bash
make update
```

## Test

```bash
make test type=unit/integration
```

## Docker

```bash
make build-container-image
```

```bash
make get-container-info-environment
make run-container-tests type=unit
```
