from fastapi import UploadFile

from app.resource.response.error_response import ErrorDetail


class UserProfileRequest:
    async def validation(self, profile: str, image: UploadFile):
        errors = []

        profile_result = await self.profile_validator(profile)
        if isinstance(profile_result, ErrorDetail):
            errors.append(profile_result)

        image_result = await self.validate_image(image)
        if isinstance(image_result, ErrorDetail):
            errors.append(image_result)

        if errors != []:
            return errors  # ErrorDetailのリストを返す
        return None

    async def profile_validator(self, value):
        if len(value) > 130:
            return ErrorDetail(
                loc=["profile"],
                msg="130文字以下である必要があります。",
                type="value_error",
            )
        return value

    async def validate_image(self, image: UploadFile):
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
