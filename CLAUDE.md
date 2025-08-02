# camply-web

A full-stack application to help you find campsites at sold-out campgrounds.

## Project Structure

This is a monorepo with two main components:

- **Backend**: FastAPI Python application (`backend/`)
- **Frontend**: React TypeScript application (`frontend/`)

## Technology Stack

### Backend

- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Key Dependencies**: Pydantic, Uvicorn, Gunicorn
- **Linting**: Ruff
- **Type Checking**: MyPy
- **Testing**: Pytest with coverage

### Frontend

- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Linting**: ESLint
- **Testing**: Vitest with Testing Library
- **Formatting**: Prettier

## Development Commands

All commands use Task (Taskfile) for consistent execution across the project.

### Installation

```bash
task install          # Install all dependencies (backend + frontend)
task backend:install  # Install backend dependencies only
task frontend:install # Install frontend dependencies only
```

### Development

```bash
task dev              # Run full stack development (backend + frontend)
task backend:debug    # Run backend in debug mode
task frontend:dev     # Run frontend development server
task run              # Run with Docker Compose
```

### Testing

```bash
task test             # Run all tests (backend + frontend)
task backend:test     # Run backend tests only
task frontend:test    # Run frontend tests only
```

### Code Quality

```bash
task lint             # Lint all code (backend + frontend)
task backend:lint     # Lint backend code only
task frontend:lint    # Lint frontend code only

task check            # Run type checking (backend + frontend)
task backend:check    # Run backend type checking (MyPy)
task frontend:check   # Run frontend type checking (TypeScript)

task fix              # Fix all code with linters and formatters
task backend:fix      # Fix backend code (Ruff)
task frontend:fix     # Fix frontend code (ESLint + Prettier)
```

### Building

```bash
task build            # Build all project artifacts
task backend:build    # Build backend artifacts
task frontend:build   # Build frontend artifacts
```

### Other

```bash
task version          # Get/Set project versions
task pre-commit       # Run pre-commit hooks
task publish          # Publish project artifacts (CI only)
```

## Project Configuration

- **Backend Config**: `backend/pyproject.toml`
- **Frontend Config**: `frontend/package.json`
- **Main Taskfile**: `Taskfile.yaml`
- **Docker**: `docker-compose.yaml`

## Development Workflow

1. Install dependencies: `task install`
2. Start development servers: `task dev`
3. Run tests: `task test`
4. Lint and format code: `task fix`
5. Type check: `task check`

## Docker

The project includes Docker configuration for both development and production deployment via Docker Compose.
