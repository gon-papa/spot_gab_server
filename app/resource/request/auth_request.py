from datetime import date as Date

from fastapi import Form
from pydantic import BaseModel, Field, field_validator

from app.resource.request.common_validate import CustomValidator
from app.resource.util.lang import convert_lang


class SignUpRequest(BaseModel):
    account_name: str = Field(
        ...,
        title="アカウント名",
        description="アカウント名",
    )
    id_account: str = Field(
        ...,
        title="アカウントID",
        description="アカウントID",
    )
    email: str = Field(
        ...,
        title="メールアドレス",
        description="メールアドレス",
    )
    password: str = Field(
        ...,
        title="パスワード",
        description="パスワード",
    )
    birth_date: Date = Field(
        ...,
        title="生年月日",
        description="生年月日",
    )

    @field_validator("account_name", "id_account", "email")
    def name_length_validator(cls, value):
        if len(value) < 1:
            raise ValueError(convert_lang("auth.validation.required"))
        if len(value) >= 100:
            raise ValueError(convert_lang("auth.validation.max_length_100"))
        return value

    @field_validator("email")
    def email_validator(cls, value):
        return CustomValidator.email_validator(cls, value)

    @field_validator("password")
    def password_validator(cls, value):
        return CustomValidator.password_validator(cls, value)

    @field_validator("birth_date")
    def birth_date_validator(cls, value):
        if value > Date.today():
            raise ValueError(convert_lang("auth.validation.invalid_future_date"))
        if value.year < 1900:
            raise ValueError(convert_lang("auth.validation.invalid_date"))
        return value


class EmailExistsRequest(BaseModel):
    email: str = Field(
        ...,
        title="メールアドレス",
        description="メールアドレス",
    )


class IdAccountExistsRequest(BaseModel):
    id_account: str = Field(
        ...,
        title="アカウントID",
        description="アカウントID",
    )


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        title="リフレッシュトークン",
        description="リフレッシュトークン",
    )


class ResetPasswordRequest(BaseModel):
    email: str = Field(
        ...,
        title="メールアドレス",
        description="メールアドレス",
    )

    @field_validator("email")
    def email_validator(cls, value):
        return CustomValidator.email_validator(cls, value)


class ResetPasswordVerifyRequest(BaseModel):
    password: str = Form(
        ...,
        title="パスワード",
        description="パスワード",
    )

    @field_validator("password")
    def password_validator(cls, value):
        return CustomValidator.password_validator(cls, value)