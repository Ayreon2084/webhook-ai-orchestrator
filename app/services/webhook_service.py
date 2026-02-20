import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.enums import WebhookRequestStatus, WebhookSource
from app.db.models.webhook import WebhookRequest
from app.schemas.webhook import TelegramWebhook


class WebhookUnauthorized(Exception):
    def __init__(self, message: str = "Invalid or missing webhook secret") -> None:
        self.message = message
        super().__init__(self.message)


class WebhookService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._logger = logging.getLogger(__name__)

    async def handle_telegram_webhook(
        self, payload: TelegramWebhook, secret_token: str | None
    ) -> dict:
        if secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
            raise WebhookUnauthorized()

        # TODO: Implement idempotency check using Telegram update_id.
        # If update_id exists, return existing correlation_id and skip insert.
        correlation_id = str(uuid.uuid4())
        self._logger.info(
            "[%s] Webhook received. Update ID: %s",
            correlation_id,
            payload.update_id,
        )

        record = WebhookRequest(
            correlation_id=correlation_id,
            source=WebhookSource.TELEGRAM,
            payload=payload.model_dump(mode="json"),
            status=WebhookRequestStatus.PENDING,
        )
        self._session.add(record)
        await self._session.flush()

        # TODO: For scaling: push task to queue (Redis/Celery) and return 200; worker persists and processes.
        return {"status": "accepted", "correlation_id": correlation_id}
