from datetime import datetime

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import WebhookRequestStatus, WebhookSource
from app.db.base import Base


class WebhookRequest(Base):
    __tablename__ = "webhook_requests"

    correlation_id: Mapped[str] = mapped_column(index=True)
    source: Mapped[WebhookSource] = mapped_column(
        SQLEnum(
            WebhookSource,
            name="webhook_source_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=WebhookSource.TELEGRAM,
        server_default=WebhookSource.TELEGRAM.value,
    )
    payload: Mapped[dict] = mapped_column(JSONB)
    status: Mapped[WebhookRequestStatus] = mapped_column(
        SQLEnum(
            WebhookRequestStatus,
            name="webhook_request_status_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=WebhookRequestStatus.PENDING,
        server_default=WebhookRequestStatus.PENDING.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
