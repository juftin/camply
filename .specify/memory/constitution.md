<!--
<sync_impact_report>
- Version change: N/A → 1.0.0
- List of modified principles: All initialized from template.
- Added sections: Technology Stack & Constraints, Development Workflow & Quality Gates.
- Removed sections: None.
- Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated/verified)
    - .specify/templates/spec-template.md (✅ updated/verified)
    - .specify/templates/tasks-template.md (✅ updated/verified)
- Follow-up TODOs: None.
</sync_impact_report>
-->

# camply Constitution

## Core Principles

### I. Reliability & Precision

Campsite availability is time-sensitive and competitive. The system MUST provide accurate, up-to-date information. Every availability check MUST be verified against the provider's API. Notifications SHOULD be delivered within 60 seconds of detection to ensure user competitiveness.

### II. Type Safety & Static Analysis

To prevent runtime errors in a complex multi-provider system, strict typing and static analysis are non-negotiable. No PR shall be merged with `mypy` errors (backend) or `tsc` errors (frontend). `ruff` (backend) and `eslint` (frontend) linting violations MUST be resolved before implementation is considered complete.

### III. Modern Workflow & Automation

Developer experience and environment consistency are critical for maintainability. All development operations (install, test, lint, build, deploy) MUST be accessible via `task`. Environment consistency MUST be maintained via `uv` for Python and `Docker` for containerized services.

### IV. Monorepos & Separation of Concerns

The project structure MUST maintain clear boundaries between `backend/`, `frontend/`, and the legacy `cli/`. Shared logic MUST be extracted into internal packages within the `backend/packages/` workspace to ensure reusability and testability without tight coupling.

### V. Automated Verification

Software correctness MUST be empirically verified. Every new feature or bug fix MUST include unit tests. Integration tests MUST be provided for all third-party provider integrations (e.g., recreation.gov, usedirect) using VCR-style cassettes or mocks where appropriate to ensure reliable CI.

## Technology Stack & Constraints

- **Backend**: Python 3.9+ managed by `uv`. FastAPI for web services. SQLAlchemy/Alembic for persistence.
- **Frontend**: React 18+ with TypeScript, built via Vite. Tailwind CSS for styling.
- **Infrastructure**: Docker & Docker Compose for local development and orchestration.
- **Task Orchestration**: `go-task` (Taskfile) is the unified entry point for all project commands.

## Development Workflow & Quality Gates

1. **Research & Design**: All significant features MUST start with a specification (`spec.md`) and implementation plan (`plan.md`).
2. **Constitution Check**: Implementation plans MUST be audited against these principles before coding begins.
3. **Test-First Mentality**: Identify testing strategies during the design phase. Verify that tests fail before implementing the fix/feature.
4. **CI/CD Alignment**: Local `task lint`, `task check`, and `task test` MUST pass before pushing to remote branches.

## Governance

This Constitution serves as the foundational authority for engineering standards within the `camply` project.

1. **Supremacy**: In cases of architectural ambiguity, these principles take precedence over "just-in-case" alternatives or legacy patterns.
2. **Amendments**: Any contributor may propose amendments. Changes require a version increment (MAJOR for principle removals, MINOR for additions, PATCH for clarifications) and a Sync Impact Report.
3. **Compliance**: Compliance is verified during Peer Review and via automated CI gates. Complexity introduced by violating a principle MUST be explicitly justified in the Implementation Plan.

**Version**: 1.0.0 | **Ratified**: 2026-03-22 | **Last Amended**: 2026-03-22
