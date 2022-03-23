FROM python:3.8-slim-bullseye

COPY src /app/src/
COPY tests /app/tests/
COPY .git /app/.git/
COPY [".isort.cfg", ".pre-commit-config.yaml", "Makefile", "poetry.lock", "pyproject.toml", "/app/"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_VERSION 22.0.4
ENV POETRY_VERSION 1.1.13
ENV HADOLINT_VERSION 1.18.0

RUN apt-get update && \
    apt-get -y install --no-install-recommends git=1:2.30.2-1 && \
    apt-get -y install --no-install-recommends make=4.3-4.1 && \
    apt-get -y install --no-install-recommends wget=1.21-1+deb11u1 && \
    wget -q -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v${HADOLINT_VERSION}/hadolint-Linux-x86_64 && \
    chmod +x /bin/hadolint && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --no-cache-dir pip==${PIP_VERSION} && \
    pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    make --directory /app/ setup-environment && \
    make --directory /app/ info-environment
