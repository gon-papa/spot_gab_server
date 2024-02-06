import re
from pydantic import BaseModel, Field, field_validator
from datetime import date as Date

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
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, value):
            raise ValueError('メールアドレスが無効です。正しい形式で入力してください。')
        return value
    
    @field_validator('password')
    def password_validator(cls, value):
        if len(value) < 8:
            raise ValueError('8文字以上である必要があります。')
        if len(value) >= 20:
            raise ValueError('最大100文字までです。')
        # 半角英数字と記号のみ
        if not re.match(r'^[@?$%!#0-9a-zA-Z]+$', value):
            raise ValueError('パスワードは半角英数字と記号 @?$%!# のみです。')
        return value
    
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