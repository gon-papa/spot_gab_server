import re
from pydantic import BaseModel, Field, field_validator
from app.resource.request.common_validate import CustomValidator


class UserProfileRequest(BaseModel):
    account_name: str = Field(
        ...,
        title="アカウント名",
        description="アカウント名",
    )
    link: str = Field(
        None,
        title="リンク",
        description="リンク",
        json_schema_extra={'nullable': True}
    )
    profile: str = Field(
        None,
        title="プロフィール",
        description="プロフィール",
        json_schema_extra={'nullable': True}
    )
    image_uuid: str = Field(
        None,
        title="画像UUID",
        description="画像UUID",
        json_schema_extra={'nullable': True}
    )

    @field_validator("account_name")
    def required_validate(cls, value):
        return CustomValidator.requreid_validator(cls, value)
    
    @field_validator("account_name")
    def account_name_validate(cls, value):
        if len(value) > 100:
            raise ValueError("100文字以内で入力してください")
        return value
    
    @field_validator("link")
    def link_validate(cls, value):
        if (value is None) or (value == ""):
            return value
        if len(value) > 1024:
            raise ValueError("1024文字以内で入力してください")
        # url形式
        if not re.match(r"https?://([\w\-]+\.)+[\w\-]+(/[\w\- ./?%&=]*)?", value):
            raise ValueError("URL形式で入力してください")
        return value

    @field_validator("profile")
    def profile_validate(cls, value):
        if (value is None) or (value == ""):
            return value
        if len(value) > 130:
            raise ValueError("130文字以内で入力してください")
        return value