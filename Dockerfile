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
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 
    # paths
    # this is where our requirements + virtual environment will live
    #PYSETUP_PATH="/opt/pysetup" \
    #VENV_PATH="/opt/pysetup/.venv"
# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apk add bash
RUN apk add openssh
RUN apk add make
RUN apk add git
RUN apk add alpine-sdk
RUN apk add curl
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN apk add sqlite-dev

# Install Terraform
ENV TERRAFORM_VERSION=1.4.6
RUN curl -LO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Install poetry
RUN curl -sSL --insecure https://install.python-poetry.org | python3 -

COPY ./entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh
RUN mkdir /opt/deployer

COPY src /root/src
RUN chown root:root -R /root/src
# Solve dependencies
#RUN poetry config experimental.new-installer false
RUN cd /root/src; poetry install

ENTRYPOINT /root/entrypoint.sh