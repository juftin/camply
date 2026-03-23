# AGENT_TROUBLESHOOTING: Common Issues & Solutions

This document helps agents and contributors resolve common environment and runtime issues encountered during the development of `camply`.

## 🛠️ Infrastructure Issues

### 1. "Valkey Connection Refused" or "Broker Connection Error"
- **Cause**: The Valkey container is not running or the worker can't reach it.
- **Solution**:
    - Ensure Docker is running: `docker compose ps`.
    - Restart infrastructure: `docker compose up -d valkey`.
    - Check `.env`: Ensure `REDIS_URL` points to `redis://localhost:6379/0`. (Note: Celery uses the `redis://` protocol even for Valkey).

### 2. "Postgres: Password Authentication Failed"
- **Cause**: Local DB credentials mismatch.
- **Solution**:
    - Check `DATABASE_URL` in `.env`.
    - If needed, reset the DB container: `docker compose down -v db && docker compose up -d db`.

---

## 🐍 Backend (Python) Issues

### 3. "Alembic: Multiple Heads Detected"
- **Cause**: Two agents created migrations simultaneously.
- **Solution**:
    - Run `uv run alembic merge heads` to create a new merge migration.
    - Or, delete the conflicting migration if it hasn't been pushed yet.

### 4. "VCR Cassette Missing" or "No Match Found"
- **Cause**: A new provider test was added but the API response wasn't recorded.
- **Solution**:
    - Run the test with record mode: `task backend:test -- --vcr-record=new_episodes`.
    - Ensure you have the necessary API keys in your `.env`.

---

## ⚛️ Frontend (React) Issues

### 5. "TypeScript Error: Module './lib/api' has no exported member..."
- **Cause**: The frontend SDK is out of sync with the FastAPI backend.
- **Solution**:
    - Ensure the backend is running.
    - Run the codegen: `task frontend:codegen`.

### 6. "Auth0: Callback URL Mismatch"
- **Cause**: Local dev URL (`http://localhost:5173`) isn't allowed in the Auth0 dashboard.
- **Solution**:
    - Add `http://localhost:5173/auth/callback` to "Allowed Callback URLs" in your Auth0 Application settings.
    - Or, switch to `AUTH_MODE=local` for non-auth testing.

---

## 🤖 Agent Workflow Issues

### 7. "Git Worktree Conflict"
- **Cause**: Trying to create a worktree for a branch that is already checked out.
- **Solution**:
    - Check existing worktrees: `git worktree list`.
    - Use a unique name: `git worktree add .worktrees/feature-v2 -b feature-v2`.

### 8. "Pre-Commit Hook Failure"
- **Cause**: Linting or formatting errors detected on commit.
- **Solution**:
    - Run `task fix` to automatically resolve most issues.
    - Review manual fixes for type errors (`mypy`/`tsc`).
