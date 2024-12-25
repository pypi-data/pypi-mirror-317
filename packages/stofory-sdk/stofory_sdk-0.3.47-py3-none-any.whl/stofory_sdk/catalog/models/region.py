from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import SlugKey, AuditColumns, CommonTableAttributes, orm_registry
from sqlalchemy import Index, UniqueConstraint, Sequence
from sqlalchemy.dialects.postgresql import VARCHAR, ENUM, TEXT, BOOLEAN, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr, DeclarativeBase

from .enums.location import LocationType
from .enums.part_of_world import PartOfWorldType

if TYPE_CHECKING:
    from .product import Product


class SmallIntPrimaryKey:
    """BigInt Primary Key Field Mixin."""

    # noinspection PyMethodParameters
    @declared_attr
    def id(cls) -> Mapped[int]:
        """BigInt Primary key column."""
        return mapped_column(
            SMALLINT,
            Sequence(f"{cls.__tablename__}_id_seq", optional=False),  # type: ignore[attr-defined]
            primary_key=True,
        )


class SmallIntAuditBase(CommonTableAttributes, SmallIntPrimaryKey, AuditColumns, DeclarativeBase):
    """Base for declarative models with BigInt primary keys and audit columns."""

    registry = orm_registry


# https://www.artlebedev.ru/country-list/
class Region(SmallIntAuditBase):
    @declared_attr.directive
    @classmethod
    def __table_args__(cls):
        return (
            UniqueConstraint("alpha2", name="uq_region_alpha2"),
            UniqueConstraint("alpha3", name="uq_region_alpha3"),
            Index("idx_alpha2", "alpha2"),
            Index("idx_alpha3", "alpha3"),
        )

    # id: Mapped[int] = mapped_column(
    #     SMALLINT,
    #     Sequence(f"region_id_seq", optional=False),
    #     primary_key=True
    # )

    name_ru: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False
    )
    name_en: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False
    )
    alpha2: Mapped[str] = mapped_column(
        VARCHAR(2),
        nullable=False
    )
    alpha3: Mapped[str] = mapped_column(
        VARCHAR(3),
        nullable=False
    )
    iso: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False
    )

    part_of_world: Mapped[str] = mapped_column(
        ENUM(PartOfWorldType, name="part_of_world_enum"),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        ENUM(LocationType, name="location_enum"),
        nullable=True,
    )

    product_bought: Mapped[list["Product"]] = relationship(
        lazy="noload",
        back_populates="region_buy",
    )

    # products_sold: Mapped[list["Product"]] = relationship(
    #     lazy="noload",
    #     back_populates="regions_sale",
    # )
