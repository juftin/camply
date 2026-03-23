# CONFIGURATION: Environment Variables & Settings

This document defines all environment variables used by the `camply` monorepo. Agents and contributors should use this as a reference when setting up local or production environments.

## ⚙️ Core Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment stage (`local`, `development`, `production`) | `local` |
| `DEBUG` | Enable debug logs and FastAPI docs | `true` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://camply:camply@localhost:5432/camply` |
| `VALKEY_URL` | Valkey connection string for Celery | `redis://localhost:6379/0` |

---

## 🔒 Authentication (Toggleable)

`camply` supports two authentication modes.

### 1. Auth0 Mode (Community/SaaS)
Enabled when `AUTH_MODE=auth0`.
| Variable | Description |
|----------|-------------|
| `AUTH_MODE` | Set to `auth0` to enable external identity provider. |
| `AUTH0_DOMAIN` | Your Auth0 tenant domain (e.g., `dev-xyz.us.auth0.com`). |
| `AUTH0_AUDIENCE` | The API Identifier configured in Auth0. |
| `AUTH0_CLIENT_ID` | The Frontend Application Client ID. |

### 2. Local-Only Mode (Private Self-Hosting)
Enabled when `AUTH_MODE=local`.
| Variable | Description |
|----------|-------------|
| `AUTH_MODE` | Set to `local` to bypass external auth. |
| `ADMIN_EMAIL` | The email address that will automatically be whitelisted. |

---

## 🔔 Notifications

### Pushover (MVP)
| Variable | Description |
|----------|-------------|
| `PUSHOVER_APP_TOKEN` | The API Token for your Pushover "Application". |

### Apprise (Legacy/Future)
| Variable | Description |
|----------|-------------|
| `APPRISE_URLS` | Comma-separated list of Apprise-compatible URLs. |

---

## 📈 Monitoring & Observability

### Sentry
| Variable | Description |
|----------|-------------|
| `SENTRY_DSN` | The DSN for error tracking (Optional). |
| `SENTRY_TRACES_SAMPLE_RATE` | Percentage of traces to capture (0.0 to 1.0). |

---

## 🏗️ Docker & Infrastructure
These variables are primarily used in `docker-compose.yaml`.
| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | DB Username | `camply` |
| `POSTGRES_PASSWORD` | DB Password | `camply` |
| `POSTGRES_DB` | DB Name | `camply` |
| `BACKEND_VERSION` | Docker image tag for backend | `local` |
| `FRONTEND_VERSION` | Docker image tag for frontend | `local` |
