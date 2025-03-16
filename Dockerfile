FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY ./pyproject.toml ./
COPY ./.git ./.git
COPY ./blumenladen ./blumenladen

USER root

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    git

RUN uv sync

EXPOSE 8080
CMD ["uv", "run", "uvicorn", "blumenladen.api:start_server"]