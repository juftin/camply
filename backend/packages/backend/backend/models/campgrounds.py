from pydantic import BaseModel


class Campground(BaseModel):
    """
    Campground Model
    """

    id: str
    provider_id: int
    recreation_area_id: str | None
    name: str
    description: str | None
    country: str | None
    state: str | None
    longitude: float | None
    latitude: float | None
    reservable: bool = True
    enabled: bool = True
