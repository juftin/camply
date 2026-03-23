# camply: Path Forward

This document outlines the strategic roadmap for transitioning `camply` from a legacy CLI tool to a modern, full-stack, community-facing web application for campsite availability monitoring.

## 🎯 Vision
A **free, open-source, and self-hostable** campsite availability scanner. Users can create accounts, set up high-frequency "scans" for specific parks/dates, and receive real-time alerts via **Pushover** (and other channels) when a spot opens up.

## 🏗️ Core Architecture & Standards
- **Backend**: FastAPI (Python 3.12, `uv` workspace) using **Pydantic v2**.
- **Frontend**: React (TypeScript, Vite, Tailwind CSS + **Shadcn/UI**).
- **Database**: PostgreSQL (SQLAlchemy + Alembic).
- **Worker**: Smart **De-duplicated Poller** (Celery + Valkey) for high-frequency scanning without API pressure.
- **Auth**: Multi-user **Auth0** integration with a **Local DB Whitelist**. Auth0 MUST be toggleable (via `.env`) to support simple local-only self-hosting without external identity providers.
- **Licensing**: Transition to a **Non-Commercial License** (e.g., Polyform Non-Commercial or AGPL with restrictions) to prevent unauthorized paid hosting/monetization.
- **Notifications**: Initial support for **Pushover** (extensible to Email/Discord).

- **Monitoring**: **Sentry** integration enabled for error tracking and performance.
- **Infrastructure**: **Docker Compose** + **Kubernetes** manifests.
- **API Strategy**: OpenAPI/Swagger with automated TypeScript client generation for the frontend.
- **Standards**: 
    - **Testing**: `pytest` (Backend) and `vitest` (Frontend) with VCR recordings for external APIs.
    - **Typing**: Strict static analysis with `mypy` and `tsc`.
    - **Local Dev**: Unified orchestration via `Docker Compose` and `Taskfile.yaml`.

---

## 🚀 Strategic Feature Requirements

### 1. High-Frequency Scanning
- **Sub-Minute Polling**: Architect the worker to support scan intervals as low as 30-45 seconds for highly competitive parks.
- **Provider-Specific Intervals**: Allow different default intervals based on provider "politeness" policies.

### 2. Granular Filtering
- **Equipment Specifics**: Filter by RV/Trailer length and type.
- **Site Attributes**: Filter by "Electric Only", "Full Hookups", "Pull-through", or "Pets Allowed".
- **Specific Site Monitoring**: Allow users to watch specific campsite numbers within a facility.
- **Minimum Stay Logic**: Only alert if a consecutive block of `X` nights is found.

### 3. Discovery & UX
- **Global Search**: Unified search across all providers (Recreation.gov, State Parks, etc.).
- **Map-Based Discovery**: (Future) Integrate maps to help users find campgrounds near specific areas.
- **Permit Monitoring**: Extend scanning logic to support Wilderness/Backcountry permits and Tours.

---

## 🛤️ Roadmap Phases

### Phase 1: Smart Poller & Single-Scan MVP
**Goal**: Build the "Smart" engine that de-duplicates requests and proves the end-to-end flow.
- [ ] **DB Schema**: Design `Users` (with early access flag), `UniqueTargets` (unique definitions), and `UserScans` (user subscriptions).
- [ ] **Sentry**: Initialize Sentry SDKs for both Backend and Frontend.
- [ ] **Provider Engine**: Define the new `BaseProvider` ABC and migrate `recreation_dot_gov` logic.
- [ ] **Celery Worker**: Implement de-duplicated polling logic in Celery.
- [ ] **Infrastructure**: Update `docker-compose.yaml` to include Valkey and Celery worker/beat services.
- [ ] **Tooling**: Add Celery/Worker management tasks to the `backend/Taskfile.yaml`.
- [ ] **OpenAPI**: Expose initial search/scan endpoints and configure client generation.
- [ ] **Pushover**: Integrate basic notification delivery.


### Phase 2: User Dashboard & Auth
**Goal**: Enable secure, multi-user management of scans.
- [ ] **Auth0**: Implement login/signup and whitelist verification flow.
- [ ] **Scan Management**: Build a dashboard to create, pause, and delete user-specific scans.
- [ ] **Frontend Refactor**: Update `package.json` scripts and dependency management.
- [ ] **Dockerization**: Update `docker-compose.yaml` and `Dockerfile` for optimized frontend builds.
- [ ] **User Config**: Secure storage for user-specific Pushover keys and notification preferences.
- [ ] **Validation**: Ensure strict schema validation for all user-provided scan parameters.

### Phase 3: Provider Parity & Advanced Filtering
**Goal**: Full feature parity with the legacy CLI and advanced scanning features.
- [ ] **Providers**: Port `usedirect`, `going_to_camp`, `xanterra`.
- [ ] **Advanced Filters**: Implement RV length, electric, and accessibility filters in the worker.
- [ ] **Permits**: Add support for scanning wilderness permit and tour availability.

### Phase 4: Production & Scale
**Goal**: Finalize for deployment and community use.
- [ ] **Rate Limiting**: Implement proxy rotation and intelligent backoff strategies.
- [ ] **Observability**: Prometheus/Grafana monitoring for scan success rates and queue latency.
- [ ] **Polish**: Full mobile-responsive UI/UX with Shadcn/UI refinements.

---

## 📝 Interactive Discussion Points

1. **Notification Costs**: SMS sending costs money. Should we prioritize free channels (Email, Push, Discord/Telegram) first before implementing SMS?
2. **Provider API Limits**: Competitive services use extensive proxying to avoid getting banned. How sophisticated do we want to make our request engine initially?
3. **Scan Limits**: Should we limit the number of active scans a user can have at once to manage server load?
4. **Data Retention**: How long should we keep history of campsite availability data?

---

## 🏁 Next Immediate Steps
1. [ ] **Database Design**: Create SQLAlchemy models for the Multi-User / De-duplicated architecture in `backend/packages/db`.
2. [ ] **Provider Migration**: Extract search logic from `cli/` to `backend/packages/providers/`.
3. [ ] **API Scaffolding**: Setup OpenAPI client generation in the frontend.
