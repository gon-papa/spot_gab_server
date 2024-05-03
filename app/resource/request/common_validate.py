import re
from typing import List
from fastapi import File

from app.resource.util.lang import convert_lang
from app.resource.response.error_response import ErrorDetail


class CustomValidator:
    @staticmethod
    def requreid_validator(cls, value):
        if value is None or value == "":
            raise ValueError(convert_lang("auth.validation.required"))
        return value
    
    @staticmethod
    def email_validator(cls, value):
        email_regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.match(email_regex, value):
            raise ValueError(convert_lang("auth.validation.invalid_email"))
        return value

    @staticmethod
    def password_validator(cls, value):
        if len(value) < 8:
            raise ValueError(convert_lang("auth.validation.min_length_8"))
        if len(value) >= 20:
            raise ValueError(convert_lang("auth.validation.max_length_20"))
        # 半角英数字と記号のみ
        if not re.match(r"^[@?$%!#0-9a-zA-Z]+$", value):
            raise ValueError(convert_lang("auth.validation.invalid_password"))
        return value

    @staticmethod
    async def validate_image(images: List):
        errors = []
        if images == []:
            errors.append(
                ErrorDetail(
                    loc=["image"],
                    msg="ファイルが選択されていません。",
                    type="value_error",
                )
            )
        for image in images:
            if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
                errors.append(
                    ErrorDetail(
                        loc=["image"],
                        msg="jpeg,jpg,png形式である必要があります。",
                        type="value_error",
                    )
                )
            data = await image.read()
            if len(data) > 10_000_000:
                errors.append(
                    ErrorDetail(
                        loc=["image"],
                        msg="10MB以下である必要があります。",
                        type="value_error",
                    )
                )
            image.file.seek(0)
        # エラーがあればエラーを配列で返す
        return errors
