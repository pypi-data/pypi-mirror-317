from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, ENUM

from .enums import ContentType

if TYPE_CHECKING:
    from .product_platform import ProductPlatform


class ProductPlatformContent(BigIntAuditBase):
    __table_args__ = (
        Index("idx_product_platform_content_product_platform_id", "product_platform_id"),
    )

    product_platform_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("product_platform.id", ondelete="CASCADE"),
                                                     nullable=False)
    content_type: Mapped[ContentType] = mapped_column(ENUM(ContentType, name="content_type_enum"), nullable=False)
    value: Mapped[str] = mapped_column(TEXT, nullable=False)    # Could be actual content or URL to file

    product_platform: Mapped[ProductPlatform] = relationship(
        back_populates="contents",
        foreign_keys="ProductPlatformContent.product_platform_id",
        innerjoin=True,
        uselist=False,
        lazy="noload"
    )
