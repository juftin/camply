from abc import ABC

from pydantic import AliasChoices, BaseModel, Field

from providers.base import DatabasePopulator, NullHandler


class Address(NullHandler):
    """
    Model representing a facility address.
    """

    Id: int | str = Field(validation_alias=AliasChoices("FacilityID", "RecAreaID"))
    City: str | None
    AddressType: str = Field(
        validation_alias=AliasChoices("FacilityAddressType", "RecAreaAddressType")
    )
    AddressStateCode: str | None
    PostalCode: int | str | None
    AddressCountryCode: str | None


class AddressData(BaseModel):
    """
    Model representing a facility address.
    """

    RECDATA: list[Address]

    def to_mapping(self) -> dict[int | str, Address]:
        """
        Convert the list of facility addresses to a mapping.
        """
        return {
            address.Id: address
            for address in self.RECDATA
            if address.AddressType == "Default"
        }


class AddressPopulator(DatabasePopulator, ABC):
    """
    Populator for facility addresses.
    """

    ADDRESSES: dict[int | str, Address] = Field(default_factory=dict)
