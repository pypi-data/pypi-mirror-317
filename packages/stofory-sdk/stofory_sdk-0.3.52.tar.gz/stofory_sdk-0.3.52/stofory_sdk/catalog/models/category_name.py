from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from .category import Category
    from .localization import Localization


class CategoryName(BigIntAuditBase):
    __table_args__ = (
        Index("idx_category_name_category_id", "category_id"),
        Index("idx_category_name_localization_id", "localization_id"),
    )

    category_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    localization_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("localization.id", ondelete="CASCADE"), nullable=False)
    value: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    category: Mapped[Category] = relationship(
        back_populates="names",
        foreign_keys="CategoryName.category_id",
        innerjoin=True,
        uselist=False,
        lazy="noload"
    )

    locale: Mapped[Localization] = relationship(
        back_populates="category_names",
        foreign_keys="CategoryName.localization_id",
        innerjoin=True,
        uselist=False,
        lazy="joined"
    )
