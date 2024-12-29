from __future__ import annotations

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY, ENUM
from sqlalchemy.orm import Mapped, mapped_column

from .enums import SyncTaskType, SyncTaskPriority


class SyncQueueMapping(BigIntAuditBase):
    priority: Mapped[SyncTaskPriority] = mapped_column(ENUM(SyncTaskPriority, name="sync_task_priority_enum"), nullable=False)
    consumer: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    table_names: Mapped[list[str]] = mapped_column(ARRAY(VARCHAR(255)), nullable=False)
    operation: Mapped[SyncTaskType] = mapped_column(ENUM(SyncTaskType, name="sync_task_type_enum"), nullable=False)
