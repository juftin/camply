# DEVELOPER_GUIDE: Getting Started

This guide walks you through setting up the `camply` development environment.

## 📋 Prerequisites
- **Python 3.12+** (Managed via [uv](https://github.com/astral-sh/uv))
- **Node.js 18+** (Managed via `npm`)
- **Docker & Docker Compose**
- **go-task** (The [Taskfile](https://taskfile.dev) runner)

---

## 🚀 Quick Start (Local Setup)

1.  **Clone & Install**:
    ```bash
    git clone https://github.com/juftin/camply.git
    cd camply
    task install
    ```

2.  **Configure Environment**:
    - Create a `.env` file in the root based on [docs/CONFIGURATION.md](CONFIGURATION.md).
    - For simple local testing, set `AUTH_MODE=local`.

3.  **Start the Stack**:
    ```bash
    # This starts Postgres, Valkey, and the Celery Worker
    docker compose up -d db redis worker
    
    # This starts the FastAPI backend and Vite frontend in watch mode
    task dev
    ```

4.  **Access the App**:
    - **Frontend**: `http://localhost:5173`
    - **API Docs**: `http://localhost:8000/api/docs`

---

## 🛠️ Common Workflows

### 1. Database Migrations
We use Alembic for backend migrations.
- **Generate**: `task backend:migration -- "your message"`
- **Apply**: `task backend:migration-upgrade`

### 2. Provider Migration
When porting logic from the legacy `cli/` to the new `backend/packages/providers`:
1.  Define the internal Pydantic models in `models/`.
2.  Implement the `BaseProvider` interface.
3.  Add unit tests using `pytest-vcr` to record initial API responses.

### 3. API & Client Generation
If you change a FastAPI router:
1.  Verify the backend types: `task backend:check`.
2.  Update the frontend SDK: `task frontend:codegen`.

---

## 🧪 Testing Discipline

### Backend
- Run all tests: `task backend:test`
- Update VCR cassettes: `task backend:test -- --vcr-record=all`

### Frontend
- Run vitest: `task frontend:test`
- Type check: `task frontend:check`

---

## ✅ Pre-Commit & Linting
The project uses `pre-commit` to ensure code quality.
- Run manually: `task pre-commit`
- Auto-fix issues: `task fix`
