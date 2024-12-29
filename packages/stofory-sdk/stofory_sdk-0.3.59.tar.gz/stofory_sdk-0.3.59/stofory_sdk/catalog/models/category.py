from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase, SlugKey
from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import VARCHAR, BIGINT, BOOLEAN
from sqlalchemy.orm import Mapped, relationship, mapped_column, declared_attr
from sqlalchemy_utils import LtreeType

from .decorator.ltree_str import LtreeStr

if TYPE_CHECKING:
    from .product_platform_category import ProductPlatformCategory
    from .category_name import CategoryName


class Category(BigIntAuditBase):
    __table_args__ = (
        Index("idx_category_platform_id", "platform_id"),
        Index("idx_gist_path", "path", postgresql_using='gist'),
    )

    platform_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("platform.id", ondelete="CASCADE"), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(BIGINT, ForeignKey("category.id"), nullable=True)
    path: Mapped[str] = mapped_column(LtreeStr, nullable=False)
    # name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    external_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True)
    external_parent_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True)
    is_owner: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    is_subcategory: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    product_platform_info_categories: Mapped[list[ProductPlatformCategory]] = relationship(
        back_populates="category",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
    )

    names: Mapped[list[CategoryName]] = relationship(
        back_populates="category",
        lazy="selectin",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan",
    )
