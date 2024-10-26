# Use the official Python image from the Docker Hub for building
FROM python:3.12.4-slim AS builder

# Install Poetry
RUN pip install poetry==1.8.4

# Set the environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory in the builder stage
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the builder stage
COPY pyproject.toml poetry.lock ./

# Install the project dependencies in the builder stage
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# Use a minimal Python image for the final stage
FROM python:3.12.4-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY app /app/app/

# Expose the port your app runs on (if applicable)
EXPOSE 8000
CMD ["fastapi", "run"]
