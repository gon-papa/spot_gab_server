import re
from fastapi import UploadFile

from app.resource.response.error_response import ErrorDetail


class UserProfileRequest:
    async def validation(self, accountName: str, link: str, profile: str, image: UploadFile):
        errors = []

        accountNameResult = await self.accountName_validator(accountName)
        if isinstance(accountNameResult, ErrorDetail):
            errors.append(accountNameResult)

        linkResult = await self.link_validator(link)
        if isinstance(linkResult, ErrorDetail):
            errors.append(linkResult)

        profile_result = await self.profile_validator(profile)
        if isinstance(profile_result, ErrorDetail):
            errors.append(profile_result)

        image_result = await self.validate_image(image)
        if isinstance(image_result, ErrorDetail):
            errors.append(image_result)

        if errors != []:
            return errors  # ErrorDetailのリストを返す
        return None

    async def accountName_validator(self, value):

        if (value is None) or (value == ""):
            return ErrorDetail(
                loc=["accountName"],
                msg="アカウント名を入力してください",
                type="value_error",
            )
        if len(value) > 100:
            return ErrorDetail(
                loc=["accountName"],
                msg="100文字以下である必要があります。",
                type="value_error",
            )
        return value

    async def link_validator(self, value):
        if (value is None) or (value == ""):
            return value
        if len(value) > 1024:
            return ErrorDetail(
                loc=["link"],
                msg="1024文字以下である必要があります。",
                type="value_error",
            )
        # url形式
        if not re.match(r"https?://([\w\-]+\.)+[\w\-]+(/[\w\- ./?%&=]*)?", value):
            return ErrorDetail(
                loc=["link"],
                msg="URL形式で入力してください。",
                type="value_error",
            )
        return value

    async def profile_validator(self, value):
        if (value is None) or (value == ""):
            return value
        if len(value) > 130:
            return ErrorDetail(
                loc=["profile"],
                msg="130文字以下である必要があります。",
                type="value_error",
            )
        return value

    async def validate_image(self, image: UploadFile):
        if image is None:
            return image
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            return ErrorDetail(
                loc=["image"],
                msg="jpeg形式である必要があります。",
                type="value_error",
            )
        data = await image.read()
        if len(data) > 10_000_000:
            return ErrorDetail(
                loc=["image"],
                msg="10MB以下である必要があります。",
                type="value_error",
            )
        image.file.seek(0)  # ファイルポインタをリセット
        return data
