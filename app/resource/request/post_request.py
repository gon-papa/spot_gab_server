
from decimal import Decimal
from typing import Optional
from fastapi import Form
from pydantic import BaseModel, Field, field_validator

from app.resource.request.common_validate import CustomValidator


# formデータをモデルに変換する
async def get_post_form_data(
    body: str = Form(..., example="こんにちは"),
    lat: float = Form(..., example=35.689487),
    lng: float = Form(..., example=139.691706),
    point: str = Form(..., example="POINT(139.691706 35.689487)"),
    geo_hash: str = Form(..., example="xn7n7"),
    country: Optional[str] = Form(None),
    administrative_area: Optional[str] = Form(None),
    sub_administrative_area: Optional[str] = Form(None),
    locality: Optional[str] = Form(None),
    sub_locality: Optional[str] = Form(None),
    postal_code: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    street: Optional[str] = Form(None),
    iso_country_code: Optional[str] = Form(None),
    thoroughfare: Optional[str] = Form(None),
    sub_thoroughfare: Optional[str] = Form(None)
):
    return PostRequest(
        body=body, lat=lat, lng=lng, point=point, geo_hash=geo_hash,
        country=country, administrative_area=administrative_area,
        sub_administrative_area=sub_administrative_area, locality=locality,
        sub_locality=sub_locality, postal_code=postal_code, name=name,
        street=street, iso_country_code=iso_country_code,
        thoroughfare=thoroughfare, sub_thoroughfare=sub_thoroughfare
    )


class PostRequest(BaseModel):
    body: str = Field(
        ...,
        title="投稿本文",
        description="投稿本文",
        examples=["こんにちは"],
    )
    lat: Decimal = Field(
        ...,
        title="緯度",
        description="緯度",
        examples=[35.689487],
    )
    lng: Decimal = Field(
        ...,
        title="経度",
        description="経度",
        examples=[139.691706],
    )
    point: str = Field(
        ...,
        title="位置情報",
        description="位置情報",
        examples=["POINT(139.691706 35.689487)"],
    )
    geo_hash: str = Field(
        ...,
        title="ジオハッシュ",
        description="ジオハッシュ",
        examples=["xn7n7"],
    )
    country: Optional[str] = Field(
        ...,
        title="国",
        description="国",
        examples=["日本"],
    )
    administrative_area: Optional[str] = Field(
        ...,
        title="都道府県",
        description="都道府県",
        examples=["群馬県"],
    )
    sub_administrative_area: Optional[str] = Field(
        ...,
        title="市区町村",
        description="市区町村",
        examples=["太田市"],
    )
    locality: Optional[str] = Field(
        ...,
        title="市区町村",
        description="市区町村",
        examples=["太田市"],
    )
    sub_locality: Optional[str] = Field(
        ...,
        title="町名",
        description="町名",
        examples=["新田木崎町"],
    )
    postal_code: Optional[str] = Field(
        ...,
        title="郵便番号",
        description="郵便番号",
        examples=["370-0321"],
    )
    name: Optional[str] = Field(
        ...,
        title="地名",
        description="地名",
        examples=["東京タワー"],
    )
    street: Optional[str] = Field(
        ...,
        title="住所",
        description="住所",
        examples=["日本、〒370-0321 群馬県太田市新田木崎町"],
    )
    iso_country_code: Optional[str] = Field(
        ...,
        title="ISO国コード",
        description="ISO国コード",
        examples=["JP"],
    )
    thoroughfare: Optional[str] = Field(
        ...,
        title="通り",
        description="通り",
        examples=["新田上江田尾島線"],
    )
    sub_thoroughfare: Optional[str] = Field(
        ...,
        title="番地",
        description="番地",
        examples=["1-1-1"],
    )
    
    @field_validator('body', 'lat', 'lng', 'point', 'geo_hash')
    def requreid_validator(cls, v):
        return CustomValidator.requreid_validator(cls, v)

    @field_validator('lat')
    def validate_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('緯度は-90から90の間でなければなりません。')
        return v

    @field_validator('lng')
    def validate_longitude(cls, v):
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