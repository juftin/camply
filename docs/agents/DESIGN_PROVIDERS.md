# DESIGN_PROVIDERS: Provider Architecture & Logic Migration

This document outlines the architecture for the provider layer in `camply`, focusing on a standardized interface, provider-specific Pydantic models, and the logic migration from the legacy CLI.

## 🎯 Architecture Goals
1. **Standardization**: All providers must return a unified `CampsiteDTO` to the worker.
2. **Isolation**: Each provider maintains its own internal Pydantic models (matching the source API).
3. **Translation**: Explicit translation layers (`to_campsite`) convert raw API data to the unified DTO.
4. **Maintenance**: Background tasks for periodic metadata updates (Park names, locations, types).

---

## 🏗️ Core Interface: `BaseProvider`

Every provider must inherit from this ABC to ensure compatibility with the **Smart Poller**.

```python
class BaseProvider(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        """Unique slug: e.g., 'recreation_dot_gov'"""
        pass

    @abstractmethod
    async def find_availabilities(
        self, 
        park_id: str, 
        start_date: date, 
        end_date: date
    ) -> List[CampsiteDTO]:
        """
        The primary scan method. 
        Calls internal API, parses into internal models, 
        and translates to CampsiteDTO.
        """
        pass

    @abstractmethod
    async def sync_metadata(self) -> None:
        """
        Background task to update the 'Search' and 'Campground' 
        tables with the latest info from the provider.
        """
        pass
```

---

## 📦 The Unified DTO: `CampsiteDTO`

This is the only object the **Worker** ever sees.

- `campsite_id`: `String` (Unique within provider)
- `campsite_name`: `String`
- `campsite_type`: `CampsiteType` (Enum: TENT, RV, CABIN, etc.)
- `capacity`: `Integer`
- `available_dates`: `List[Date]`
- `is_electric`: `Boolean`
- `is_accessible`: `Boolean`
- `metadata`: `Dict[String, Any]` (Provider-specific raw attributes)

---

## 🔄 Logic Migration Strategy

Instead of wrapping the legacy `cli/` code, we are migrating the core "Scraping" logic to ensure it fits our new **async-first** and **multi-tenant** architecture.

### 1. Internal Pydantic Models
We will copy and refine the Pydantic models from `cli/camply/containers/api_responses.py` into each provider's `models/` subdirectory. 
*Example*: `backend/packages/providers/recreation_gov/models/api.py`.

### 2. The Translation Layer
Each internal API model will implement a conversion method:

```python
class RecDotGovCampsite(PydanticBaseModel):
    # ... raw API fields ...
    
    def to_dto(self) -> CampsiteDTO:
        return CampsiteDTO(
            campsite_id=str(self.campsite_id),
            campsite_name=self.name,
            # ... mapping logic ...
        )
```

---

## 🛠️ Background Tasks

To keep the system running smoothly, providers are responsible for more than just scanning:

1. **Metadata Refresh**: 
   - *Frequency*: Weekly.
   - *Task*: Download full campground lists (e.g., RIDB export for Recreation.gov) and update the `Search` table so users can find new parks in the UI.
2. **Stale Result Cleanup**:
   - *Frequency*: Daily.
   - *Task*: Purge entries from `scan_results` that are in the past or no longer relevant.
3. **Provider Health Check**:
   - *Frequency*: Hourly.
   - *Task*: Perform a "noop" search to ensure the provider API hasn't changed its structure or blocked our IP.

---

## 🔒 Performance & Concurrency
- **Connection Pooling**: Use a shared `httpx.AsyncClient` within the provider package.
- **Async-First**: All IO-bound operations must be `async` to prevent blocking the worker.
- **Rate Limiting**: Implementation of provider-specific backoff logic to respect API limits.
