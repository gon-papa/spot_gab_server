import re
from datetime import date as Date


def email_validator(cls, value):
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(email_regex, value):
        raise ValueError('メールアドレスが無効です。正しい形式で入力してください。')
    return value
    
def password_validator(cls, value):
        if len(value) < 8:
            raise ValueError('8文字以上である必要があります。')
        if len(value) >= 20:
            raise ValueError('最大100文字までです。')
        # 半角英数字と記号のみ
        if not re.match(r'^[@?$%!#0-9a-zA-Z]+$', value):
            raise ValueError('パスワードは半角英数字と記号 @?$%!# のみです。')
        return value