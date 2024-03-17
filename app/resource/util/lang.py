import i18n
from typing import Optional
from app.resource.middleware.http import current_language


# ミドルウェアで設定された言語を取得する
def get_current_language():
    return current_language.get()


# i18nの言語変換を行う keyは言語ファイル名.key名
def convert_lang(key: str, lang: Optional[str] = None) -> str:
    lang = lang if lang else get_current_language()
    return i18n.t(key, locale=get_current_language())
