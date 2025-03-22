# Blumenladen

![License: Apache 2.0](https://img.shields.io/github/license/huyenngn/blumenladen)
![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)

Automations for my mom's flower shop.

## Features

- [x] Fetch data from invoices sent to email
- [x] Parse invoices and extract product information and expenses
- [x] Store data in database
- [x] Dashboard for viewing inventory and expenses data
- [x] German UI
- [ ] Vietnamese UI

![Image](https://github.com/user-attachments/assets/42464fba-8707-493a-953b-64d54d4e8d81)
![Image](https://github.com/user-attachments/assets/6e283ec1-7d19-4794-b60e-b530dbfd590e)
![Image](https://github.com/user-attachments/assets/f4832c02-b002-4c33-8f39-bfb9ce936930)

## Prerequisites

Apple requires **app-specific passwords** for third-party apps to access iCloud email accounts. To generate an app-specific password, follow the instructions [here](https://support.apple.com/en-us/HT204397).

## Quickstart

Run the following commands to set the necessary environment variables:

```sh
export EMAIL_ACCOUNT=your-email-account
export APP_PASSWORD=your-app-password
```

Build and run the dashboard with Docker:

```sh
docker compose build
docker compose up -d
```

Open your browser at `http://localhost`.

## Development

Use [uv](https://docs.astral.sh/uv/) to set up a local development environment.

```sh
git clone https://github.com/huyenngn/blumenladen.git
cd blumenladen
uv sync
```

You can use `uv run <command>` to avoid having to manually activate the project
venv. For example, to start the backend dev server, run:

```sh
uv run dev
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
