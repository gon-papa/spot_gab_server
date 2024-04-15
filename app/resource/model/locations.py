from datetime import datetime, timezone
from typing import Optional
from decimal import Decimal
from uuid import uuid4
from geoalchemy2 import Geometry
from sqlalchemy import Numeric
from sqlmodel import SQLModel, Column, Integer, Field, String, TIMESTAMP


class Locations(SQLModel, table=True):
    __tablename__ = "locations"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    uuid: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String(36), nullable=False, unique=True, comment="UUID")
    )
    lat: Decimal = Field(
        default=None,
        sa_column=Column(Numeric(10, 8), nullable=False, comment="緯度")
    )
    lng: Decimal = Field(
        default=None,
        sa_column=Column(Numeric(11, 8), nullable=False, comment="経度")
    )
    point: str = Field(
        default=None,
        sa_column=Column(Geometry(geometry_type="POINT", srid=4326), nullable=False, comment="位置情報")
    )
    geo_hash: str = Field(
        default=None,
        sa_column=Column(String(12), nullable=False, comment="ジオハッシュ")
    )
    srid: str = Field(
        default=None,
        sa_column=Column(String(10), nullable=False, comment="SRID")
    )
    save_datetime: datetime = Field(sa_column=Column(TIMESTAMP(True), nullable=True, comment="保存日時"))
    country: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="国")
    )
    administrative_area: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="都道府県")
    )
    sub_administrative_area: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="市区町村(日本は無い場合が多い)")
    )
    locality: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="市区町村")
    )
    sub_locality: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="町名(日本は無い場合が多い)")
    )
    postal_code: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="郵便番号")
    )
    name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="地名")
    )
    street: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="住所")
    )
    iso_country_code: Optional[str] = Field(
        default=None,
        sa_column=Column(String(10), nullable=True, comment="ISO国コード")
    )
    thoroughfare: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="通り")
    )
    sub_thoroughfare: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, comment="番地")
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(True),
            nullable=True,
            default=datetime.now(timezone.utc)
        )
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(True),
            nullable=True,
            onupdate=datetime.now(timezone.utc)
        )
    )