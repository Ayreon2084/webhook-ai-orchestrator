import uvicorn
from fastapi import FastAPI

from app.api.v1.routers import api_v1_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(api_v1_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
