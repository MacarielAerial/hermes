#
# Multi Stage: Dev Image
#
FROM python:3.12-slim-bookworm AS dev

# Set environemntal variables
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_HOME=/home/poetry \
    PYTHONUNBUFFERED=1

# Add poetry executable to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl

# Install poetry
RUN mkdir -p /home/poetry && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry self add poetry-plugin-up

# Verify Poetry installation
RUN poetry --version

#
# Multi Stage: Bake Image
#

FROM python:3.12-slim-bookworm AS bake

# Set environemntal variables
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_HOME=/home/poetry \
    PYTHONUNBUFFERED=1

# Add poetry executable to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install curl
RUN apt-get update && apt-get install -y \
    curl

# Install poetry
RUN mkdir -p /home/poetry && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry self add poetry-plugin-up

# Verify Poetry installation
RUN poetry --version

# Make working directory
RUN mkdir -p /app

# Only copy necessary files when implemented
COPY pyproject.toml poetry.lock /app/

# Set working directory
WORKDIR /app

# Install python dependencies in container
RUN poetry install --without dev

#
# Multi Stage: Runtime Image
#

FROM python:3.12-alpine AS runtime

# Copy over baked environment
# Explicitly copy the otherwise ignore .venv folder
COPY --from=bake /app /app
COPY --from=bake /app/.venv /app/.venv

# Set 
WORKDIR /app

# Set executables in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Bake the health check into the image
HEALTHCHECK --interval=10s --timeout=5s --retries=3 --start-period=5s CMD curl --fail http://localhost:80/health || exit 1

# TODO: Add a command to start the service
ENTRYPOINT ["fastapi", "run", "app/main.py", "--port", "80"]
