from fastapi import APIRouter, Header, HTTPException, status

from app.api.deps import WebhookServiceDep
from app.schemas.webhook import TelegramWebhook
from app.services.webhook_service import WebhookUnauthorized


router = APIRouter()


@router.post("/telegram")
async def handle_telegram_webhook(
    webhook_data: TelegramWebhook,
    webhook_service: WebhookServiceDep,
    x_telegram_bot_api_secret_token: str | None = Header(None),
):
    """
    Store webhook payload in DB for further processing.
    Validates X-Telegram-Bot-Api-Secret-Token (set via setWebhook).
    """
    try:
        return await webhook_service.handle_telegram_webhook(
            webhook_data, x_telegram_bot_api_secret_token
        )
    except WebhookUnauthorized as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message
        )
