from functools import cached_property

from pydantic import BaseModel, computed_field

from providers import PROVIDERS
from providers.base import BaseProvider


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

    @cached_property
    def provider(self) -> type[BaseProvider]:
        """
        Get the provider instance for this campground.
        """
        return PROVIDERS[self.provider_id]

    @computed_field
    def url(self) -> str:
        return self.provider.get_campground_url(campground_id=self.id)
