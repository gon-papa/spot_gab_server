from datetime import datetime, timezone
from injector import inject

from app.resource.model.user_locations import UserLocations
from app.resource.model.users import Users
from app.resource.repository.user_location_repository import UserLocationRepository
from app.resource.request.user_location_request import UserLocationRequest


class UserLocationSercice:
    @inject
    def __init__(
        self,
        repository: UserLocationRepository,
    ):
        self.repository = repository

    async def save_location(self, request: UserLocationRequest, current_user: Users):
        location = UserLocations(
            user_id=current_user.id,
            lat=request.lat,
            lng=request.lng,
            point=f"POINT({request.lat} {request.lng})",
            geo_hash=request.geo_hash,
            srid="4326",
            save_datetime=datetime.now(timezone.utc),
            administrative_area=request.administrative_area,
            sub_administrative_area=request.sub_administrative_area,
            locality=request.locality,
            sub_locality=request.sub_locality,
            postal_code=request.postal_code,
            name=request.name,
            street=request.street,
            iso_country_code=request.iso_country_code,
            country=request.country,
            thoroughfare=request.thoroughfare,
            sub_thoroughfare=request.sub_thoroughfare,
        )

        return await self.repository.save_location(location)
