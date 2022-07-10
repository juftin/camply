from typing import Any, List

from camply.containers.base_container import CamplyModel


class ResourceLocation(CamplyModel):
    """
    /api/resourcelocation/rootmaps
    """

    ID: int | None
    RecAreaID: int
    ParkAlerts: Any  # TODO this will be a string, but some extraction will need to be done on the API respones first
    ResourceCategories: None | List[int]
    ResourceLocationID: int | None
    ResourceLocationName: str
