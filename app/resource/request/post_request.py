
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field, field_validator

from app.resource.request.common_validate import CustomValidator


class PostRequest(BaseModel):
    body: str = Field(
        ...,
        title="投稿本文",
        description="投稿本文",
        examples=["こんにちは"],
    )
    hashtags: List[str] = Field(
        ...,
        title="ハッシュタグ",
        description="ハッシュタグ",
        examples=[["#hello", "#world"]],
        json_schema_extra={'nullable': True}
    )
    images: List[str] = Field(
        ...,
        title="画像",
        description="画像",
        examples=[["path", "path"]],
        json_schema_extra={'nullable': True}
    )
    lat: str = Field(
        ...,
        title="緯度",
        description="緯度",
        examples=['35.689487'],
    )
    lng: str = Field(
        ...,
        title="経度",
        description="経度",
        examples=['139.691706'],
    )
    point: str = Field(
        ...,
        title="位置情報",
        description="位置情報",
        examples=["POINT(35.689487 139.691706)"],
    )
    geo_hash: str = Field(
        ...,
        title="ジオハッシュ",
        description="ジオハッシュ",
        examples=["xn7n7"],
    )
    country: str = Field(
        ...,
        title="国",
        description="国",
        examples=["日本"],
        json_schema_extra={'nullable': True}
    )
    administrative_area: str = Field(
        ...,
        title="都道府県",
        description="都道府県",
        examples=["群馬県"],
        json_schema_extra={'nullable': True}
    )
    sub_administrative_area: str = Field(
        ...,
        title="市区町村",
        description="市区町村",
        examples=["太田市"],
        json_schema_extra={'nullable': True}
    )
    locality: str = Field(
        ...,
        title="市区町村",
        description="市区町村",
        examples=["太田市"],
        json_schema_extra={'nullable': True}
    )
    sub_locality: str = Field(
        ...,
        title="町名",
        description="町名",
        examples=["新田木崎町"],
        json_schema_extra={'nullable': True}
    )
    postal_code: str = Field(
        ...,
        title="郵便番号",
        description="郵便番号",
        examples=["370-0321"],
        json_schema_extra={'nullable': True}
    )
    name: str = Field(
        ...,
        title="地名",
        description="地名",
        examples=["東京タワー"],
        json_schema_extra={'nullable': True}
    )
    street: str = Field(
        ...,
        title="住所",
        description="住所",
        examples=["日本、〒370-0321 群馬県太田市新田木崎町"],
        json_schema_extra={'nullable': True}
    )
    iso_country_code: str = Field(
        ...,
        title="ISO国コード",
        description="ISO国コード",
        examples=["JP"],
        json_schema_extra={'nullable': True}
    )
    thoroughfare: str = Field(
        ...,
        title="通り",
        description="通り",
        examples=["新田上江田尾島線"],
        json_schema_extra={'nullable': True}
    )
    sub_thoroughfare: str = Field(
        ...,
        title="番地",
        description="番地",
        examples=["1-1-1"],
        json_schema_extra={'nullable': True}
    )
    
    @field_validator('body', 'lat', 'lng', 'point', 'geo_hash')
    def requreid_validator(cls, v):
        return CustomValidator.requreid_validator(cls, v)

    @field_validator('lat')
    def validate_latitude(cls, v):
        v = Decimal(v)
        if not (-90 <= v <= 90):
            raise ValueError('緯度は-90から90の間でなければなりません。')
        return v

    @field_validator('lng')
    def validate_longitude(cls, v):
        v = Decimal(v)
        if not (-180 <= v <= 180):
            raise ValueError('経度は-180から180の間でなければなりません。')
        return v

    @field_validator('point')
    def validate_point(cls, v):
        import re
        pattern = r"POINT\(\s*(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s*\)"
        if not re.match(pattern, v):
            raise ValueError('位置情報は"POINT(経度 緯度)"の形式でなければなりません。')
        return v
