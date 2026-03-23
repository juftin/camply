# DESIGN_API: API Contract & Security

This document defines the interface between the `camply-backend` (FastAPI) and `camply-frontend` (React). It also outlines the security flow for Auth0 and early access whitelisting.

## 🎯 API Philosophy
1. **OpenAPI-First**: Every endpoint must be documented so that the frontend TypeScript client can be automatically generated.
2. **Standardized Responses**: All successful responses use `ORJSONResponse` for performance.
3. **Strict Validation**: Every request payload must be a Pydantic v2 model.
4. **Auth-Gated**: All user-specific endpoints require a valid Auth0 JWT.

---

## 🔒 Security & Middleware

### 1. Auth0 Authentication
- **Token Source**: Frontend sends the Auth0 JWT in the `Authorization: Bearer <token>` header.
- **Backend Verification**: `VerifyToken` dependency validates the signature and issuer against Auth0.

### 2. Early Access (Whitelist) Middleware
- **Check**: For every request to `/api/v1/scans/*`, the backend checks the `email` from the JWT against the `users.is_early_access_user` flag.
- **Action**: If the user is not whitelisted, the backend returns `403 Forbidden` with a custom error code `ERR_EARLY_ACCESS_REQUIRED`.
- **UI Interaction**: The frontend catches `403` and redirects the user to the "Request Access" landing page.

---

## 🏗️ Endpoint Definitions

### 1. Search & Metadata (Public/Auth-Light)
- **`GET /api/v1/search?term=<query>`**: Search for campgrounds and recreation areas.
- **`GET /api/v1/providers`**: List supported providers and their scanning capabilities.

### 2. User & Profile (Auth-Required)
- **`GET /api/v1/me`**: Get current user profile and whitelist status.
- **`PATCH /api/v1/me`**: Update user-specific settings (e.g., `pushover_token`).

### 3. Scan Management (Auth-Required + Whitelist)
- **`GET /api/v1/scans`**: List all scans belonging to the current user.
- **`POST /api/v1/scans`**: Create a new scan.
    - **Logic**: Backend calculates the target `hash`, creates/links the `UniqueTarget`, and creates the `UserScan`.
- **`GET /api/v1/scans/{id}`**: Detailed view of a scan, including recent `scan_results`.
- **`PATCH /api/v1/scans/{id}`**: Update scan filters (e.g., `min_stay_length`) or toggle `is_active`.
- **`DELETE /api/v1/scans/{id}`**: Unsubscribe from a scan.

---

## 📦 Request / Response DTOs (Pydantic)

### Example: `ScanCreate`
```python
class ScanCreate(BaseModel):
    provider_id: str
    park_id: str
    start_date: date
    end_date: date
    min_stay_length: int = 1
    preferred_types: List[str] = []
    require_electric: bool = False
```

### Example: `ScanSummary`
```python
class ScanSummary(BaseModel):
    id: UUID
    park_name: str
    start_date: date
    end_date: date
    is_active: bool
    last_checked_at: Optional[datetime]
    found_count: int  # Number of matching campsites currently available
```

---

## 🔄 Client Generation Workflow
1. Backend developer updates the FastAPI router.
2. Run `task check` to ensure types are correct.
3. Frontend runs `task frontend:codegen` which:
    - Starts the backend temporarily.
    - Fetches `http://localhost:8000/api/openapi.json`.
    - Generates a fresh TypeScript SDK in `frontend/src/lib/api/`.
4. Frontend developers use the generated hooks (e.g., `useGetScansQuery()`).
