"""
camply-backend FastAPI Application
"""

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from camply_backend.__about__ import __application__, __version__
from camply_backend.routers.health import health_router

app = FastAPI(
    title=__application__,
    version=__version__,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
    default_response_class=ORJSONResponse,
)

API_ROUTERS: list[APIRouter] = [
    health_router,
]

for router in API_ROUTERS:
    app.include_router(router, prefix="/api")


def main() -> None:  # pragma: no cover
    """
    API Server Entry Point
    """
    import uvicorn

    uvicorn.run(
        app="camply_backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
