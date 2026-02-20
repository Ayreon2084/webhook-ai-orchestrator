"""FastAPI dependencies: session and service factories."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.services.webhook_service import WebhookService


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_webhook_service(session: SessionDep) -> WebhookService:
    return WebhookService(session)


WebhookServiceDep = Annotated[WebhookService, Depends(get_webhook_service)]
