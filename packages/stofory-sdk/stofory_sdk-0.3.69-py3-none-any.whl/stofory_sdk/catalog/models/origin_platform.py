from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase, SlugKey
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

if TYPE_CHECKING:
    from .product import Product


class OriginPlatform(BigIntAuditBase, SlugKey):
    @declared_attr.directive
    @classmethod
    def __table_args__(cls):
        return (
            UniqueConstraint("name", name="uq_origin_platform_name"),
            Index("idx_origin_platform_name", "name"),
            UniqueConstraint(
                cls.slug,
                name=f"uq_{cls.__tablename__}_slug",
            ).ddl_if(callable_=cls._create_unique_slug_constraint),
            Index(
                f"ix_{cls.__tablename__}_slug_unique",
                cls.slug,
                unique=True,
            ).ddl_if(callable_=cls._create_unique_slug_index),
        )

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False
    )

    products: Mapped[list[Product]] = relationship(
        back_populates="origin_platform",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan"
    )
