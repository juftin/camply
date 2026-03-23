# DESIGN_AGENTIC: Local Development & Agentic Tooling

This document outlines the local "Agentic" development environment for `camply`. These Model Context Protocol (MCP) servers allow AI agents (like Gemini CLI) to interact directly with the database, UI, and infrastructure for autonomous implementation and validation.

## 🎯 Philosophy
1. **Local-First**: All tools run locally to ensure privacy, speed, and reliability.
2. **Autonomous Validation**: The agent should be able to *prove* a change works (e.g., query the DB or run a browser test) before finishing a task.
3. **Task-Driven**: Tools are integrated into the `spec-kit` workflow to automate the boring parts (issue tracking, documentation lookup).

---

## 🛠️ MCP Configuration (Local Dev)

The following MCP servers should be added to the local agent configuration (e.g., `gemini-cli` config or `claude_desktop_config.json`).

### 1. Database MCP (PostgreSQL)
**Capability**: Directly query the local `camply` database.
- **Connection**: `postgresql://postgres:postgres@localhost:5432/camply`
- **Use Case**:
    - Verify schema migrations.
    - Validate de-duplication logic (hashes).
    - Insert/Update whitelisted users for early access testing.

### 2. Browser MCP (Playwright)
**Capability**: Launch and control a local browser instance.
- **URL**: `http://localhost:5173` (Vite Frontend)
- **Use Case**:
    - "Visual Regression": Confirm Shadcn/UI components look correct.
    - "E2E Testing": Automate the "Search -> Create Scan -> Dashboard" flow.
    - "Auth Testing": Verify the Auth0 redirect and early access gate.

### 3. Docker MCP
**Capability**: Monitor and manage the local container stack.
- **Stack**: `backend-api`, `celery-worker`, `redis`, `postgres`.
- **Use Case**:
    - Check Celery logs for scan errors.
    - Restart specific services after a code change.
    - Monitor queue depth in Valkey.

### 4. GitHub MCP
**Capability**: Manage issues, PRs, and project boards.
- **Repository**: `juftin/camply`
- **Use Case**:
    - Synchronize `spec-kit` tasks with GitHub Issues.
    - Create PRs with detailed "Plan vs. Reality" descriptions.
    - Automate project board transitions.

### 5. DevDocs / Search MCP
**Capability**: Real-time documentation lookup.
- **Targets**: `FastAPI`, `Pydantic v2`, `Shadcn/UI`, `Tailwind`, `Celery`.
- **Use Case**:
    - Ensure idiomatic usage of Shadcn primitives.
    - Reference latest Pydantic validator syntax.

---

## 🚀 Workflow Integration

### Step 1: Research
When starting a feature, the agent uses **DevDocs MCP** to find the best implementation patterns and **GitHub MCP** to audit related existing issues.

### Step 2: Strategy
The agent uses **spec-kit** to generate the plan and **Postgres MCP** to check the current DB state for conflicts.

### Step 3: Execution & Validation
1. Agent writes code.
2. Agent uses **Docker MCP** to restart the worker.
3. Agent uses **Postgres MCP** to verify data was correctly inserted into `unique_targets`.
4. Agent uses **Playwright MCP** to visually confirm the change in the UI.

### Step 4: Finalization
Agent uses **GitHub MCP** to update tasks and submit the PR.

---

## 🔒 Security & Local Config
- **Secrets**: Never store API keys in this documentation.
- **Auth0 Testing**: For local dev, we will use a dedicated "Dev" Auth0 Tenant or a mocked local Auth flow to avoid hitting production limits.
