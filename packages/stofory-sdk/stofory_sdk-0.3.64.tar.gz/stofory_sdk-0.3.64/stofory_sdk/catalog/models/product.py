from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase, SlugKey
from sqlalchemy import Index, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, ENUM, TEXT, BOOLEAN, BIGINT, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from .enums import ProductType
from .enums.product_kind import ProductKind


if TYPE_CHECKING:
    from .region import Region
    from .origin_platform import OriginPlatform
    from .product_platform import ProductPlatform
    from .product_platform_external_connection import ProductPlatformExternalConnection


class Product(BigIntAuditBase, SlugKey):
    @declared_attr.directive
    @classmethod
    def __table_args__(cls):
        return (
            Index("idx_product_name", "name"),
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

    # __table_args__ = (
    #     Index("idx_product_name", "name"),
    # )

    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[str] = mapped_column(TEXT(), nullable=False)
    product_type: Mapped[ProductType] = mapped_column(ENUM(ProductType, name='product_type_enum'), nullable=False)
    product_kind: Mapped[ProductKind] = mapped_column(ENUM(ProductKind, name='product_kind_enum'), nullable=False)
    status: Mapped[bool] = mapped_column(BOOLEAN(), default=False)

    origin_platform_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            "origin_platform.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )
    region_buy_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            "region.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )
    regions_sale_ids: Mapped[list[int]] = mapped_column(
        ARRAY(BIGINT),
        nullable=True
    )

    origin_platform: Mapped[OriginPlatform] = relationship(
        back_populates="products",
        foreign_keys="Product.origin_platform_id",
        lazy="joined",
        uselist=True,
        passive_deletes=True,
    )

    region_buy: Mapped[Region] = relationship(
        lazy="joined",
        back_populates="product_bought",
    )

    regions_sale: Mapped[list[Region]] = relationship(
        primaryjoin="Product.regions_sale_ids.any(foreign(Region.id))",
        viewonly=True,
        lazy="noload",
        # back_populates="products_sold",
    )

    product_platforms: Mapped[list[ProductPlatform]] = relationship(
        back_populates="product",
        lazy="noload",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    external_connections: Mapped[list[ProductPlatformExternalConnection]] = relationship(
        back_populates="product",
        lazy="noload",
        uselist=True,
        # cascade="all, delete-orphan"
    )


"""
CREATE OR REPLACE FUNCTION check_regions_sale_ids_exist()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, есть ли несуществующие region_id в regions_sale_ids
    IF EXISTS (
        SELECT 1
        FROM unnest(NEW.regions_sale_ids) AS region_id
        WHERE NOT EXISTS (SELECT 1 FROM region WHERE id = region_id)
    ) THEN
        RAISE EXCEPTION 'One or more regions in regions_sale_ids do not exist in the region table';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Привязываем функцию к таблице product
CREATE TRIGGER trg_check_regions_sale_ids
BEFORE INSERT OR UPDATE OF regions_sale_ids ON product
FOR EACH ROW
EXECUTE FUNCTION check_regions_sale_ids_exist();

"""