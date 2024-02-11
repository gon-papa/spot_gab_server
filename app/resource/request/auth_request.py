import re
from pydantic import BaseModel, Field, field_validator
from datetime import date as Date
from app.resource.request.common_validate import email_validator, password_validator

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
    
    @field_validator('account_name', 'id_account', 'email')
    def name_length_validator(cls, value):
        if len(value) < 1:
            raise ValueError('1文字以上である必要があります。')
        if len(value) >= 100:
            raise ValueError('最大100文字までです。')
        return value
    
    @field_validator('email')
    def email_validator(cls, value):
        return email_validator(cls, value)
    
    @field_validator('password')
    def password_validator(cls, value):
        return password_validator(cls, value)
    
    @field_validator('birth_date')
    def birth_date_validator(cls, value):
        if value > Date.today():
            raise ValueError('未来の日付は指定できません。')
        if value.year < 1900:
            raise ValueError('1900年以降の日付を指定してください。')
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
    
class SignInRequest(BaseModel):
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
    
    @field_validator('email')
    def email_validator(cls, value):
        return email_validator(cls, value)
    
    @field_validator('password')
    def password_validator(cls, value):
        return password_validator(cls, value)