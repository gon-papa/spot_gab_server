import re

from app.resource.util.lang import convert_lang


class CustomValidator:
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
