from fastapi import APIRouter

from app.api.v1.endpoints import webhook


api_v1_router = APIRouter()
api_v1_router.include_router(webhook.router, prefix="/webhooks", tags=["webhooks"])
