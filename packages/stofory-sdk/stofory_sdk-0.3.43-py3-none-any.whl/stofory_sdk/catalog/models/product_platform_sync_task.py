from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, ENUM, ARRAY, VARCHAR
from sqlalchemy.orm import relationship, Mapped

from .decorator.jsonb_dict import JSONBDict

from .enums import SyncTaskType, SyncTaskStatus

if TYPE_CHECKING:
    from .product_platform import ProductPlatform


class ProductPlatformSyncTask(BigIntAuditBase):
    __table_args__ = (
        Index("idx_product_platform_sync_task", "product_platform_id", "task_type", "status"),
    )

    product_platform_id: Mapped[int] = Column(BIGINT, ForeignKey("product_platform.id", ondelete="CASCADE"), nullable=False)
    task_type: Mapped[SyncTaskType] = Column(ENUM(SyncTaskType, name="sync_task_type_enum"), nullable=False)
    task_meta: Mapped[dict] = Column(JSONBDict, nullable=True)
    routing_keys: Mapped[list[str]] = Column(ARRAY(VARCHAR(255)), default=[])
    sub_statuses: Mapped[dict] = Column(JSONBDict, default={})
    sub_infos: Mapped[dict] = Column(JSONBDict, default={})
    status: Mapped[SyncTaskStatus] = Column(ENUM(SyncTaskStatus, name="sync_task_status_enum"), nullable=False)
    info: Mapped[str] = Column(TEXT, nullable=True)

    product_platform: Mapped[ProductPlatform] = relationship(
        back_populates="sync_tasks",
        foreign_keys="ProductPlatformSyncTask.product_platform_id",
        innerjoin=True,
        uselist=False,
        lazy="noload",
    )
