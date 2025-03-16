# Blumenladen

![License: Apache 2.0](https://img.shields.io/github/license/huyenngn/blumenladen)
![Docs](https://github.com/huyenngn/blumenladen/actions/workflows/docs.yml/badge.svg)
![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)

Automations for my mom's flower shop.

## Quickstart

Build and run the dashboard with Docker:

```sh
docker compose build
docker compose up
```

The API server will be running at `http://localhost:8080` and the frontend will be served at `http://localhost`.

## Development

Use [uv](https://docs.astral.sh/uv/) to set up a local development environment.

```sh
git clone https://github.com/huyenngn/blumenladen.git
cd blumenladen
uv sync
```

You can use `uv run <command>` to avoid having to manually activate the project
venv. For example, to start the backend server, run:

```sh
uv run start
```

To interact with the backend, send requests to `http://localhost:8080`.

To start developing the frontend, navigate to the `dashboard` directory and run:

```sh
pnpm install
pnpm dev
```

The live frontend will be served at `http://localhost:5173`.

## License

This project is licensed under the Apache License 2.0. For the full license text, see the [`LICENSE`](LICENSE) file.
