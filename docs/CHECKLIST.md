# Feature Implementation Checklist

This checklist tracks the granular progress of `camply-web`. Agents **MUST** update this file by marking tasks as completed (`[x]`) before finalizing any PR.

---

## 🛠️ Phase 1: Smart Poller & Single-Scan MVP (Current Focus)

### 1.1 Data Layer (`backend/packages/db`)
- [ ] T1.1.1 Implement `User` model with `is_early_access_user` flag.
- [ ] T1.1.2 Implement `UniqueTarget` model with unique hashing and composite keys.
- [ ] T1.1.3 Implement `UserScan` model with user-specific filters.
- [ ] T1.1.4 Implement `ScanResult` model for availability caching.
- [ ] T1.1.5 Create and run the initial Alembic migration.

### 1.2 Provider Engine (`backend/packages/providers`)
- [ ] T1.2.1 Define the `BaseProvider` ABC with standardized `find_availabilities` and `sync_metadata`.
- [ ] T1.2.2 Implement `CampsiteDTO` (Pydantic v2) for unified data transfer.
- [ ] T1.2.3 Migrate `recreation_dot_gov` logic from legacy CLI to new structure.
- [ ] T1.2.4 Implement the first `sync_metadata` for `recreation_dot_gov` (Facilities/Rec Areas).

### 1.3 Celery Worker & Poller Logic
- [ ] T1.3.1 Setup Celery + Redis infrastructure with `uv` and Docker.
- [ ] T1.3.2 Implement the `heartbeat` scheduler (every 60s).
- [ ] T1.3.3 Implement `check_target_availability` task with de-duplication and Redis locks.
- [ ] T1.3.4 Implement `send_pushover_notification` task.
- [ ] T1.3.5 Integrate `Sentry` for background task error tracking.

### 1.4 API & Frontend Foundation
- [ ] T1.4.1 Create FastAPI search endpoints (`/api/v1/search`) using existing logic.
- [ ] T1.4.2 Create scan management endpoints (`POST /api/v1/scans`, `GET /api/v1/scans`).
- [ ] T1.4.3 Initialize React frontend with Vite + Tailwind + Shadcn/UI.
- [ ] T1.4.4 Setup automated OpenAPI TypeScript client generation.
- [ ] T1.4.5 Build the basic "Search and Start Scan" UI component.

---

## 🛠️ Phase 2: Auth0 & Early Access

### 2.1 Authentication & Profile
- [ ] T2.1.1 Configure Auth0 backend integration (JWT validation).
- [ ] T2.1.2 Implement `is_early_access_user` middleware for FastAPI.
- [ ] T2.1.3 Configure Auth0 frontend integration (React SDK).
- [ ] T2.1.4 Build the User Profile page for Pushover key management.

### 2.2 Access Control
- [ ] T2.1.5 Build the "Early Access" gate/landing page for non-whitelisted users.
- [ ] T2.1.6 Implement "Request Access" logic (simple email collection/notif).

---

## 🛠️ Phase 3: Provider Parity & Advanced Features

### 3.1 Migration
- [ ] T3.1.1 Migrate `usedirect` (California State Parks, etc.).
- [ ] T3.1.2 Migrate `going_to_camp`.
- [ ] T3.1.3 Migrate `xanterra` (Yellowstone, etc.).

### 3.2 Advanced Search
- [ ] T3.2.1 Implement electric hookup and ADA accessibility filters.
- [ ] T3.2.2 Implement equipment length (RV/Trailer) validation in poller.
- [ ] T3.2.3 Implement minimum stay requirement (X nights) in poller logic.

---

## 🛠️ Phase 4: Scale, Polish, & Infrastructure

### 4.1 Stability
- [ ] T4.1.1 Implement proxy rotation logic for provider requests.
- [ ] T4.1.2 Implement backoff/retry strategy for provider API failures.
- [ ] T4.1.3 Setup Prometheus/Grafana dashboard for scan success metrics.

### 4.2 Deployment
- [ ] T4.1.4 Finalize production `docker-compose.yml`.
- [ ] T4.1.5 Create Kubernetes manifests for API and Worker scaling.
- [ ] T4.1.6 Complete a full mobile-responsive audit of the UI.
