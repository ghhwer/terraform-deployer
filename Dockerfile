FROM python:3.10.6-alpine

USER root

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

# prepend poetry to path (official installer); pip-installed poetry uses /usr/local/bin
ENV PATH="$POETRY_HOME/bin:$PATH"

# Optional private/custom PyPI or Artifactory. Defaults keep the image public-PyPI friendly.
# Prefer ./build.sh with build.local.env, or pass --build-arg USE_CUSTOM_PYPI=true ...
ARG USE_CUSTOM_PYPI=false
ARG CUSTOM_PYPI_URL=
ARG CUSTOM_PYPI_HOST=
ARG CUSTOM_PYPI_NAME=custom

RUN apk add --no-cache \
    bash \
    openssh \
    make \
    git \
    alpine-sdk \
    curl \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    sqlite-dev \
    zip \
    jq \
    gettext

# Install yq; install poetry from custom index when opted in, else official installer
RUN set -eux; \
    if [ "$USE_CUSTOM_PYPI" = "true" ]; then \
      if [ -z "$CUSTOM_PYPI_URL" ] || [ -z "$CUSTOM_PYPI_HOST" ]; then \
        echo "USE_CUSTOM_PYPI=true requires CUSTOM_PYPI_URL and CUSTOM_PYPI_HOST" >&2; \
        exit 1; \
      fi; \
      pip install yq poetry \
        -i "$CUSTOM_PYPI_URL" \
        --trusted-host "$CUSTOM_PYPI_HOST"; \
    else \
      pip install yq; \
      curl -sSL https://install.python-poetry.org | python3 -; \
    fi

# Install Terraform
ENV TERRAFORM_VERSION=1.4.6
RUN curl -LO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

COPY ./entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh
RUN mkdir /opt/deployer

COPY src /root/src
RUN chown root:root -R /root/src

# Resolve dependencies; optionally register a custom Poetry source (not committed in pyproject.toml)
RUN set -eux; \
    cd /root/src; \
    if [ "$USE_CUSTOM_PYPI" = "true" ]; then \
      poetry source add --priority=primary "$CUSTOM_PYPI_NAME" "$CUSTOM_PYPI_URL"; \
      poetry config "certificates.${CUSTOM_PYPI_NAME}.cert" false; \
    fi; \
    poetry lock; \
    poetry install

ENTRYPOINT /root/entrypoint.sh
