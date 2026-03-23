# DESIGN_DATA: Database Schema & De-duplication

This document defines the database architecture for the `camply` platform, reconciling the legacy CLI data structures with the existing `backend` FastAPI models.

## 🎯 Hierarchy Overview
The system models campsite data in a four-tier hierarchy. To handle overlapping IDs across different booking services, **Composite Primary Keys** (`id` + `provider_id`) are used for all provider-sourced entities.

1.  **Provider**: (e.g., Recreation.gov, Parks Canada).
2.  **Recreation Area**: (e.g., Yosemite National Park).
3.  **Facility (Campground)**: (e.g., Lower Pines).
4.  **Campsite**: (e.g., Site 042).

---

## 🏗️ Table Definitions (PostgreSQL)

### 1. `providers` Table (Existing)
Defines the supported booking services.
- `id`: `Integer` (Primary Key, Autoincrement)
- `name`: `String` (Unique, e.g., "recreation_dot_gov")
- `url`: `String`

### 2. `recreation_areas` Table (Existing)
- `id`: `String` (Primary Key - Provider's Internal ID)
- `provider_id`: `Integer` (Primary Key, Foreign Key -> `providers.id`)
- `name`: `String`
- `description`: `String`
- `location`: `Point` (Lat/Long)

### 3. `campgrounds` Table (Existing)
- `id`: `String` (Primary Key - Provider's Internal ID)
- `provider_id`: `Integer` (Primary Key, Foreign Key -> `providers.id`)
- `recreation_area_id`: `String` (Foreign Key -> `recreation_areas.id`)
- `name`: `String`
- `location`: `Point`

### 4. `search` Table (Existing - Flattened Search View)
An optimized table for the frontend search bar, populated via provider sync tasks.
- `id`: `String` (Primary Key - Format: `EntityType/ProviderID/RecAreaID/CampgroundID`)
- `entity_type`: `String` ("RecreationArea" or "Campground")
- `provider_name`: `String`
- `recreation_area_name`: `String` (Indexed)
- `campground_name`: `String` (Indexed)

### 5. `campsites` Table (New - Dynamic)
Stores individual site metadata. Populated during scans or full metadata syncs.
- `id`: `String` (Primary Key - Provider's Internal ID)
- `campground_id`: `String` (Primary Key, Foreign Key -> `campgrounds.id`)
- `provider_id`: `Integer` (Primary Key, Foreign Key -> `providers.id`)
- `name`: `String` (e.g., "Site 042")
- `type`: `String` (e.g., "TENT", "RV")
- `is_accessible`: `Boolean`
- `attributes`: `JSONB` (e.g., `{"electric": true, "water": false, "max_length": 35}`)

### 6. `users` Table (New)
- `id`: `UUID` (Primary Key)
- `auth0_id`: `String` (Unique)
- `email`: `String`
- `is_early_access_user`: `Boolean`
- `pushover_token`: `String` (Optional)

### 7. `unique_targets` Table (The "What" - New)
- `id`: `UUID` (Primary Key)
- `provider_id`: `Integer` (Foreign Key -> `providers.id`)
- `campground_id`: `String` (Foreign Key -> `campgrounds.id`)
- `start_date`: `Date`
- `end_date`: `Date`
- `hash`: `String` (Unique Index) - `SHA256(provider_id + campground_id + start_date + end_date)`
- `last_checked_at`: `Timestamp`

### 8. `user_scans` Table (The "Who" - New)
- `id`: `UUID` (Primary Key)
- `user_id`: `UUID` (Foreign Key -> `users.id`)
- `target_id`: `UUID` (Foreign Key -> `unique_targets.id`)
- `is_active`: `Boolean`
- **Filters**:
    - `min_stay_length`: `Integer`
    - `preferred_types`: `Array[String]`
    - `require_electric`: `Boolean`

### 9. `scan_results` Table (The Cache - New)
- `id`: `UUID` (Primary Key)
- `target_id`: `UUID` (Foreign Key -> `unique_targets.id`)
- `campsite_id`: `String` (Foreign Key -> `campsites.id`)
- `available_dates`: `Array[Date]`
- `found_at`: `Timestamp`

---

## 🔄 Reconciled Implementation Details

### Composite Keys & Foreign Keys
Because we use composite keys, all foreign key relationships MUST include both the `id` and the `provider_id`. This is already implemented in the `campgrounds -> recreation_areas` relationship in the current codebase.

### The "Search" Table Algorithm
We will continue to use the `Search.algorithm()` method (FastAPI Backend) to power the "Find a Park" input in the Shadcn UI. This table acts as a read-cache for the metadata layer.

### Metadata vs. Scan results
- **Metadata** (`recreation_areas`, `campgrounds`, `campsites`) is mostly static or updated via weekly syncs.
- **Scan results** (`scan_results`) are ephemeral and updated every few minutes by the **Smart Poller**.
- A user creates a scan against a `campground_id`, but the system notifies them about a specific `campsite_id` that belongs to that campground.
