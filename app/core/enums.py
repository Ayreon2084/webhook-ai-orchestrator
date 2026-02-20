from enum import StrEnum


class WebhookSource(StrEnum):
    TELEGRAM = "telegram"


class WebhookRequestStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
