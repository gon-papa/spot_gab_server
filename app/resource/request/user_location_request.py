
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.resource.request.common_validate import CustomValidator


class UserLocationRequest(BaseModel):
    lat: Decimal = Field(
        ...,
        title="緯度",
        description="緯度",
        examples=[35.681236],
    )
    lng: Decimal = Field(
        ...,
        title="経度",
        description="経度",
        examples=[139.767125],
    )
    geo_hash: str = Field(
        ...,
        title="ジオハッシュ",
        description="ジオハッシュ",
    )
    administrative_area: Optional[str] = Field(
        ...,
        title="都道府県",
        description="都道府県",
    )
    sub_administrative_area: Optional[str] = Field(
        ...,
        title="市区町村(日本は無い場合が多い)",
        description="市区町村(日本は無い場合が多い)",
    )
    locality: Optional[str] = Field(
        ...,
        title="市区町村",
        description="市区町村",
    )
    sub_locality: Optional[str] = Field(
        ...,
        title="町名(日本は無い場合が多い)",
        description="町名(日本は無い場合が多い)",
    )
    postal_code: Optional[str] = Field(
        ...,
        title="郵便番号",
        description="郵便番号",
    )
    name: Optional[str] = Field(
        ...,
        title="地名",
        description="地名",
    )
    street: Optional[str] = Field(
        ...,
        title="住所",
        description="住所",
    )
    country: Optional[str] = Field(
        ...,
        title="国",
        description="国",
    )
    iso_country_code: Optional[str] = Field(
        ...,
        title="ISO国コード",
        description="ISO国コード",
    )
    thoroughfare: Optional[str] = Field(
        ...,
        title="通り名",
        description="通り名",
    )
    sub_thoroughfare: Optional[str] = Field(
        ...,
        title="番地",
        description="番地",
    )

    @field_validator("lat", "lng", "geo_hash")
    def required_validator(cls, value):
        return CustomValidator.required_validator(cls, value)

    @field_validator("lat", "lng")
    def decimal_validator(cls, value):
        try:
            Decimal(value)
        except ValueError:
            raise ValueError("数値で入力してください")
        return value

    @field_validator("lat")
    def lat_validator(cls, value):
        if value < -90 or value > 90:
            raise ValueError("緯度は-90から90の間で入力してください")
        return value

    @field_validator("lng")
    def lng_validator(cls, value):
        if value < -180 or value > 180:
            raise ValueError("経度は-180から180の間で入力してください")
        return value