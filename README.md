<div align="center">
<a href="https://github.com/juftin/camply">
  <img src="https://raw.githubusercontent.com/juftin/camply/main/docs/_static/camply.svg"
    width="400" height="400" alt="camply">
</a>
</div>

**`camply`**, the campsite finder ⛺️, is a tool to help you book a campsite online. Finding
reservations at sold out campgrounds can be tough. That's where camply comes in. It searches
thousands of campgrounds across the ~~USA~~ world via the APIs of booking services like
[recreation.gov](https://recreation.gov). It continuously checks for cancellations and
availabilities to pop up - once a campsite becomes available, camply sends you a notification
to book your spot!

---

## Directory Structure

```text
📂 camply
├── README.md
├── docker-compose.yaml
├── cli/
|   ├── pyproject.toml
|   └── camply/
├── frontend/
|   ├── Dockerfile
|   ├── docker-compose.yaml
|   ├── package.json
|   ├── tsconfig.json
|   ├── src/
|   └── public/
└── backend/
    ├── Dockerfile
    ├── docker-compose.yaml
    ├── pyproject.toml
    ├── uv.lock
    └── packages/
        ├── backend/
        |   ├── pyproject.toml
        |   └── backend/
        ├── db/
        |   ├── pyproject.toml
        |   ├── migrations/
        |   └── db/
        └── providers/
            ├── pyproject.toml
            └── providers/
```

### cli

- This directory contains the legacy command-line interface (CLI) for the project.
  There will be no further development on this CLI and it can be ignored for new
  features.

### frontend

- The frontend of the application is a React application built with TypeScript.
- It uses Vite as the build tool and includes all necessary configurations for
  development and production builds.
- It leverages modern React features and libraries for state management,
  routing, and UI components.
- It uses Tailwind CSS for styling.
- The frontend should be able to be published as a static site that can be served
  by any web server.

### backend

- The backend of the application is built with Python.
- The backend is a `uv` workspace containing multiple packages:
  - `backend/`: The FastAPI application that serves the API endpoints.
  - `db/`: Contains database models and migrations.
  - `providers/`: Contains third-party API providers and integrations.
