"""
Recreation.gov Web Searching Utilities
"""

import logging
from random import uniform
from time import sleep
from typing import List, Optional, Tuple, Union

import pandas as pd

from camply.config import RecreationBookingConfig
from camply.config.search_config import EquipmentConfig, EquipmentOptions
from camply.containers import AvailableCampsite, CampgroundFacility, SearchWindow
from camply.providers import RecreationDotGov
from camply.search.base_search import BaseCampingSearch, SearchError
from camply.utils import make_list

logger = logging.getLogger(__name__)


class SearchRecreationDotGov(BaseCampingSearch):
    """
    Camping Search Object
    """

    def __init__(
        self,
        search_window: Union[SearchWindow, List[SearchWindow]],
        recreation_area: Optional[Union[List[int], int]] = None,
        campgrounds: Optional[Union[List[int], int]] = None,
        campsites: Optional[Union[List[int], int]] = None,
        weekends_only: bool = False,
        nights: int = 1,
        equipment: Optional[List[Tuple[str, Optional[int]]]] = None,
        offline_search: bool = False,
        offline_search_path: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        recreation_area: Optional[Union[List[int], int]]
            ID of Recreation Area (i.e. 2907 - Rocky Mountain National Park)
        campgrounds: Optional[Union[List[int], int]]
            Campground ID or List of Campground IDs
        campsites: Optional[Union[List[int], int]]
            Campsite ID or List of Campsite IDs
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
        nights: int
            minimum number of consecutive nights to search per campsite,defaults to 1
        equipment: Optional[List[Tuple[str, Optional[int]]]]
            List of Tuples of Equipment to Search for. An equipment tuple array looks
            like this: `[("Tent", None), ("RV", 20)]` - meaning the selected search
            looks for sites to accommodate any tent size and RVs less than or equal
            to 20 feet. Tuples contain the Equipment name and an optional equipment
            length, otherwise provide None. Equipment names include `Tent`, `RV`,
            `Trailer`, `Vehicle` and are not case-sensitive.
        offline_search: bool
            When set to True, the campsite search will both save the results of the
            campsites it's found, but also load those campsites before beginning a
            search for other campsites.
        offline_search_path: Optional[str]
            When offline search is set to True, this is the name of the file to be saved/loaded.
            When not specified, the filename will default to `camply_campsites.json`
        """
        self.campsite_finder: RecreationDotGov
        super(SearchRecreationDotGov, self).__init__(
            provider=RecreationDotGov(),
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
            offline_search=offline_search,
            offline_search_path=offline_search_path,
        )
        self._recreation_area_id = make_list(recreation_area)
        self._campground_object = campgrounds
        self.weekends_only = weekends_only
        assert (
            any(
                [
                    campsites not in [[], None],
                    campgrounds not in [[], None],
                    recreation_area is not None,
                ]
            )
            is True
        )
        self.campsites = make_list(campsites)
        self.campgrounds = self._get_searchable_campgrounds()
        self.campsite_metadata: Optional[pd.DataFrame] = None
        self.equipment: List[Tuple[str, Optional[int]]] = []
        self.equipment = self._get_searchable_equipment(equipment=equipment)

    def _get_searchable_campgrounds(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search

        This handles scenarios where a recreation area is provided instead
        of a campground list

        Returns
        -------
        searchable_campgrounds: List[int]
            List of searchable campground IDs
        """
        if self.campsites not in [(), [], None]:
            self.campsites = [int(campsite_id) for campsite_id in self.campsites]
            searchable_campgrounds = self._get_campgrounds_by_campsite_id()
        elif self._campground_object not in [(), [], None]:
            searchable_campgrounds = self._get_campgrounds_by_campground_id()
        elif self._recreation_area_id not in [(), [], None]:
            searchable_campgrounds = self._get_campgrounds_by_recreation_area_id()
        else:
            raise RuntimeError("You must provide a Campground or Recreation Area ID")
        return list(set(searchable_campgrounds))

    @classmethod
    def _get_searchable_equipment(
        cls, equipment: Optional[List[Tuple[str, Optional[int]]]]
    ) -> Optional[List[Tuple[str, Optional[int]]]]:
        """
        Sort through and validate Equipment

        Parameters
        ----------
        equipment: Optional[List[Tuple[str, Optional[int]]]]

        Returns
        -------
        Optional[List[Tuple[str, Optional[int]]]]
        """
        equipment_names = []
        final_equipment = None
        if isinstance(equipment, (list, tuple)):
            final_equipment = []
            for equipment_name, equipment_length in equipment:
                if (
                    equipment_name.lower()
                    not in EquipmentOptions.__all_accepted_equipment__
                ):
                    logger.warning(
                        f"Equipment name not recognized: {equipment_name}. This won't "
                        "be used for filtering."
                        "Acceptable options are: "
                        f"{', '.join(EquipmentOptions.__all_accepted_equipment__)}"
                    )
                else:
                    final_equipment.append((equipment_name, equipment_length))
                    equipment_names.append(equipment_name)
            if len(final_equipment) > 0:
                logger.info(
                    f"Filtering Campsites based on Equipment: {' | '.join(equipment_names)}"
                )
        return final_equipment

    def _get_campgrounds_by_campground_id(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search when provided with campground IDs

        Returns
        -------
        returned_sites: List[int]
            List of searchable campground IDs
        """
        campground_list = make_list(self._campground_object)
        facilities = self.campsite_finder.find_campgrounds(
            campground_id=campground_list
        )
        return facilities

    def _get_campgrounds_by_campsite_id(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search when provided with Campsite IDs

        Returns
        -------
        returned_sites: List[int]
            List of searchable campground IDs
        """
        campsite_list = make_list(self.campsites)
        facilities = self.campsite_finder.find_campgrounds(campsite_id=campsite_list)
        return facilities

    def _get_campgrounds_by_recreation_area_id(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search when provided with Recreation Area IDs

        Returns
        -------
        campgrounds: List[CampgroundFacility]
        """
        campgrounds = list()
        for rec_area in self._recreation_area_id:
            campground_array = self.campsite_finder.find_facilities_per_recreation_area(
                rec_area_id=rec_area
            )
            campgrounds += campground_array
        return campgrounds

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return All Monthly Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        found_campsites = list()
        if len(self.campgrounds) == 0:
            error_message = "No campgrounds found to search"
            logger.error(error_message)
            raise SearchError(error_message)
        logger.info(f"Searching across {len(self.campgrounds)} campgrounds")
        if self.campsite_metadata is None:
            self.campsite_metadata = (
                self.campsite_finder.get_internal_campsite_metadata(
                    facility_ids=[facil.facility_id for facil in self.campgrounds]
                )
            )
            logger.info(
                "Metadata fetched for %s campsites", len(self.campsite_metadata)
            )
        for index, campground in enumerate(self.campgrounds):
            for month in self.search_months:
                logger.info(
                    f"Searching {campground.facility_name}, {campground.recreation_area} "
                    f"({campground.facility_id}) for availability: "
                    f"{month.strftime('%B, %Y')}"
                )
                availabilities = self.campsite_finder.get_recdotgov_data(
                    campground_id=campground.facility_id, month=month
                )
                campsites = self.campsite_finder.process_campsite_availability(
                    availability=availabilities,
                    recreation_area=campground.recreation_area,
                    recreation_area_id=campground.recreation_area_id,
                    facility_name=campground.facility_name,
                    facility_id=campground.facility_id,
                    month=month,
                    campsite_metadata=self.campsite_metadata,
                )
                if self.campsites not in [None, []]:
                    campsites = [
                        campsite_obj
                        for campsite_obj in campsites
                        if int(campsite_obj.campsite_id) in self.campsites
                    ]
                found_campsites += campsites
                if index + 1 < len(self.campgrounds):
                    sleep(round(uniform(*RecreationBookingConfig.RATE_LIMITING), 2))
        campsite_df = self.campsites_to_df(campsites=found_campsites)
        campsite_df_validated = self._filter_date_overlap(campsites=campsite_df)
        compiled_campsite_df = self._consolidate_campsites(
            campsite_df=campsite_df_validated, nights=self.nights
        )
        equipment_filtered_campsites = self.filter_campsites_to_equipment(
            campsites=compiled_campsite_df
        )
        compiled_campsites = self.df_to_campsites(
            campsite_df=equipment_filtered_campsites
        )

        return compiled_campsites

    def filter_campsites_to_equipment(self, campsites: pd.DataFrame) -> pd.DataFrame:
        """
        Filter a Campsite DataFrame down to specified equipment

        Parameters
        ----------
        campsites: pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """
        if self.equipment is None or len(self.equipment) == 0 or len(campsites) == 0:
            return campsites
        column_names = ["campsite_id", "permitted_equipment"]
        exploded_data = campsites[column_names].explode("permitted_equipment")
        expanded_data = exploded_data["permitted_equipment"].apply(pd.Series)
        joined_data = pd.DataFrame(
            pd.concat([exploded_data, expanded_data], axis=1),
            columns=column_names + ["equipment_name", "max_length"],
        )
        joined_data["equipment_name_normalized"] = (
            joined_data["equipment_name"]
            .fillna("")
            .apply(lambda x: EquipmentConfig.EQUIPMENT_REVERSE_MAPPING[x])
        )
        equipment_types = [item[0].lower() for item in self.equipment]
        matching_equipment = joined_data[
            joined_data["equipment_name_normalized"].isin(equipment_types)
        ]
        matching_ids = []
        for equipment_name, equipment_length in self.equipment:
            matching_data = matching_equipment[
                matching_equipment["equipment_name_normalized"]
                == equipment_name.lower()
            ].copy()
            if equipment_length is not None:
                matching_data = matching_data[
                    matching_data["max_length"] >= float(equipment_length)
                ]
            matching_ids += list(matching_data["campsite_id"].unique())

        original_campsites = campsites[
            campsites["campsite_id"].isin(matching_ids)
        ].copy()
        return original_campsites
