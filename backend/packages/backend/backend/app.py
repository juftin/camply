"""
camply-backend FastAPI Application
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from backend.__about__ import __application__, __version__
from backend.routers.health import health_router
from backend.routers.search import search_router

app = FastAPI(
    title=__application__,
    version=__version__,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://camply.juftin.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_ROUTERS: list[APIRouter] = [health_router, search_router]

for router in API_ROUTERS:
    app.include_router(router, prefix="/api")


def main() -> None:  # pragma: no cover
    """
    API Server Entry Point
    """
    import uvicorn

    uvicorn.run(
        app="backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
