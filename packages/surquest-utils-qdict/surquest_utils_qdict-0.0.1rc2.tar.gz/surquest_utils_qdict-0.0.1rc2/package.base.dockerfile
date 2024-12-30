FROM python:3.13-alpine AS base

# Copy local code to the container image.
ENV DIR_PROJECT="/opt/project"
ENV DIR_SRC="/opt/project/src"
ENV DIR_TEST="/opt/project/test"
RUN mkdir -p $DIR_PROJECT
ENV HOME=$DIR_PROJECT
WORKDIR $DIR_PROJECT

# Update pip
RUN pip install --upgrade pip

COPY /pyproject.toml /$DIR_PROJECT/pyproject.toml
COPY /README.md /$DIR_PROJECT/README.md

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED=True
ENV PYTHONPATH="${DIR_SRC}:${DIR_TEST}"

# Install python packages
RUN pip install . --no-cache-dir

FROM base AS test

# Install python packages for testing
RUN pip install .[test] --no-cache-dir