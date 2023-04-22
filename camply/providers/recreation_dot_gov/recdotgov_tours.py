"""
Recreation.gov Implementation for Tours.
"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests

from camply.config import RecreationBookingConfig, RIDBConfig
from camply.containers import AvailableCampsite
from camply.containers.api_responses import (
    RecDotGovSearchResponse,
    RecDotGovSearchResult,
    TourDailyAvailabilityResponse,
    TourMonthlyAvailabilityResponse,
    TourResponse,
)
from camply.containers.base_container import CamplyModel, RecDotGovEquipment
from camply.providers.base_provider import ProviderSearchError
from camply.providers.recreation_dot_gov.recdotgov_provider import RecreationDotGovBase
from camply.utils import api_utils

logger = logging.getLogger(__name__)


class RecreationDotGovTours(RecreationDotGovBase, ABC):
    """
    Recreation.gov Implementation for Tours
    """

    resource_api_path = RIDBConfig.TOUR_API_PATH
    api_response_class = TourResponse
    api_search_result_class = RecDotGovSearchResult
    api_search_result_key = "entity_id"
    activity_name = None  # Activity Name Should't Be Propogated to Query Parameters

    @property
    @abstractmethod
    def api_search_fq(self) -> str:
        """
        API Query Parameters
        """
        pass

    @property
    @abstractmethod
    def booking_url(self) -> str:
        """
        API Endpoint
        """
        pass

    def paginate_recdotgov_campsites(
        self, facility_id: int, equipment: Optional[List[str]] = None
    ) -> List[RecDotGovSearchResult]:
        """
        Paginate through the RecDotGov Campsite Metadata
        """
        results = 0
        continue_paginate = True
        endpoint_url = api_utils.generate_url(
            scheme=RecreationBookingConfig.API_SCHEME,
            netloc=RecreationBookingConfig.API_NET_LOC,
            path="api/search",
        )
        fq_list = [
            f"asset_id:{facility_id}",
            # Currently, entity_type:tour (parent is entity_type:ticketfacility)
            # or entity_type:timedentry_tour (parent is entity_type:timedentry).
            self.api_search_fq,
        ]
        params = {
            "start": 0,
            "size": 1000,
            "fq": fq_list,
        }
        campsites: List[RecDotGovSearchResult] = []
        while continue_paginate is True:
            response = self.make_recdotgov_request_retry(
                method="GET",
                url=endpoint_url,
                params=params,
            )
            returned_data = json.loads(response.content)
            campsite_response = RecDotGovSearchResponse(**returned_data)
            campsites += campsite_response.results
            results += campsite_response.size
            params.update(start=results)
            if results == campsite_response.total:
                continue_paginate = False
        return campsites

    def make_recdotgov_availability_request(
        self,
        campground_id: int,
        month: datetime,
    ) -> requests.Response:
        """
        Make a request to the RecreationDotGov API

        Parameters
        ----------
        campground_id
        month

        Returns
        -------
        requests.Response
        """
        api_endpoint = self._rec_availability_get_endpoint(
            path=f"{campground_id}/monthlyAvailabilitySummaryView"
        )
        query_params = {
            "year": month.strftime("%Y"),
            "month": month.strftime("%m"),
            "inventoryBucket": "FIT",
        }
        return self.make_recdotgov_request(
            method="GET",
            url=api_endpoint,
            params=query_params,
        )

    @classmethod
    def make_campsite_availability_fields(
        cls,
        tour_id: int,
        booking_url_vars: Dict[str, str],
        booking_date: datetime.date,
        campsite_metadata: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate a dictionary of fields to be used in a campsite container.

        Parameters
        ----------
        tour_id: int
        booking_url_vars: Dict[str, str]
        booking_date: datetime.date
        campsite_metadata: pd.DataFrame

        Returns
        -------
        Dict[str, Any]
        """
        booking_date = datetime.combine(booking_date, time.min)
        try:
            site_name = campsite_metadata.at[tour_id, "name"]
        except LookupError:
            site_name = f"Tour #{tour_id}"
        try:
            loop_name = campsite_metadata.at[tour_id, "description"]
        except LookupError:
            loop_name = "Description not available"
        try:
            use_type = campsite_metadata.at[tour_id, "time_zone"]
        except LookupError:
            use_type = "Time zone not available"
        return {
            "booking_url": cls.booking_url.format(**booking_url_vars),  # type: ignore
            "booking_date": booking_date,
            "booking_end_date": booking_date + timedelta(days=1),
            "booking_nights": 1,
            "campsite_id": tour_id,
            "campsite_site_name": site_name,
            "campsite_loop_name": loop_name,
            "campsite_type": cls.facility_type,
            "campsite_use_type": use_type,
        }

    @classmethod
    def process_campsite_availability(
        cls,
        availability: Dict[str, Any],
        recreation_area: str,
        recreation_area_id: int,
        facility_name: str,
        facility_id: int,
        month: datetime,
        campsite_metadata: pd.DataFrame,
    ) -> List[Optional[AvailableCampsite]]:
        """
        Parse the JSON Response and return availabilities

        Parameters
        ----------
        availability: dict
            API Response
        recreation_area: str
            Name of Recreation Area
        recreation_area_id: int
            ID of Recreation Area
        facility_name: str
            Campground Facility Name
        facility_id: int
            Campground Facility ID
        month: datetime
            Month to Process
        campsite_metadata: pd.DataFrame
            Metadata Fetched from the Recreation.gov API about the Campsites

        Returns
        -------
        total_campsite_availability: List[Optional[AvailableCampsite]]
            Any monthly availabilities
        """
        total_campsite_availability: List[Optional[AvailableCampsite]] = []
        campsite_data = TourMonthlyAvailabilityResponse(**availability)
        for (
            matching_date,
            date_related_data,
        ) in campsite_data.facility_availability_summary_view_by_local_date.items():
            for (
                tour_id,
                availability_status,
            ) in date_related_data.tour_availability_summary_view_by_tour_id.items():
                if availability_status.reservable > 0:
                    fields = cls.make_campsite_availability_fields(
                        tour_id,
                        vars(availability_status),
                        matching_date,
                        campsite_metadata,
                    )
                    available_campsite = AvailableCampsite(
                        campsite_occupancy=(1, availability_status.reservable),
                        availability_status=availability_status.availability_level,
                        recreation_area=recreation_area,
                        recreation_area_id=recreation_area_id,
                        facility_name=facility_name,
                        facility_id=facility_id,
                        permitted_equipment=[],
                        campsite_attributes=[],
                        **fields,
                    )
                    total_campsite_availability.append(available_campsite)
        return total_campsite_availability

    def get_campground_ids_by_campsites(
        self, campsite_ids: List[int]
    ) -> Tuple[List[int], List[CamplyModel]]:
        """
        Retrieve a list of FacilityIDs, and Facilities from a Campsite ID List

        This implementation for tours tolerates unknown campsite_ids and mock them using known ones.

        Parameters
        ----------
        campsite_ids: List[int]
            List of Campsite IDs

        Returns
        -------
        Tuple[List[int], List[CamplyModel]]
        """
        campground_ids = []
        campgrounds = []
        unknown_ids = []
        for campsite_id in campsite_ids:
            try:
                campsite = self.get_campsite_by_id(campsite_id=campsite_id)
            except ProviderSearchError as e:
                warning_message = (
                    "Ignoring ProviderSearchError; "
                    f"be sure that this is covered by another one in the same facility: {e}"
                )
                logging.warning(warning_message)
                unknown_ids.append(campsite_id)
                continue
            campgrounds.append(campsite)
            campground_ids.append(campsite.FacilityID)
        campground_ids_unique = list(set(campground_ids))
        if unknown_ids:
            if not campground_ids_unique:
                raise ProviderSearchError(
                    "No facility can be determined from specified tours."
                )
            for unknown_id in unknown_ids:
                campsite = TourResponse(
                    TourID=unknown_id,
                    FacilityID=campground_ids_unique[0],
                    TourName=f"Tour #{unknown_id} (facility may be wrong)",
                    TourType="Unknown Tour",
                    TourDuration=0,
                    TourDescription=f"Unknown Tour #{unknown_id}",
                    TourAccessible=False,
                    CreatedDate=date.min,
                    LastUpdatedDate=date.min,
                    ATTRIBUTES=[],
                )
                campgrounds.append(campsite)
        return campground_ids_unique, list(campgrounds)


class RecreationDotGovDailyMixin(RecreationDotGovTours, ABC):
    """
    MixIn Class to Support Daily Searches in Recreation.gov Searches
    """

    @classmethod
    def get_search_months(cls, search_days: List[datetime]) -> List[datetime]:
        """
        Get the Unique Months that need to be Searched

        Returns
        -------
        search_months: List[datetime]
            Datetime Months to search for reservations
        """
        return search_days

    def make_recdotgov_availability_request(
        self,
        campground_id: int,
        month: datetime,
    ) -> requests.Response:
        """
        Make a request to the RecreationDotGov API

        Parameters
        ----------
        campground_id
        month

        Returns
        -------
        requests.Response
        """
        api_endpoint = self._rec_availability_get_endpoint(path=str(campground_id))
        query_params = {
            "date": month.strftime("%Y-%m-%d"),
        }
        return self.make_recdotgov_request(
            method="GET",
            url=api_endpoint,
            params=query_params,
        )

    @classmethod
    def process_campsite_availability(
        cls,
        availability: Dict[str, Any],
        recreation_area: str,
        recreation_area_id: int,
        facility_name: str,
        facility_id: int,
        month: datetime,
        campsite_metadata: pd.DataFrame,
    ) -> List[Optional[AvailableCampsite]]:
        """
        Parse the JSON Response and return availabilities

        Parameters
        ----------
        availability: dict
            API Response
        recreation_area: str
            Name of Recreation Area
        recreation_area_id: int
            ID of Recreation Area
        facility_name: str
            Campground Facility Name
        facility_id: int
            Campground Facility ID
        month: datetime
            Month to Process
        campsite_metadata: pd.DataFrame
            Metadata Fetched from the Recreation.gov API about the Campsites

        Returns
        -------
        total_campsite_availability: List[Optional[AvailableCampsite]]
            Any monthly availabilities
        """
        total_campsite_availability: List[AvailableCampsite] = []
        now = datetime.now(timezone.utc)
        availabilities: Dict[str, Any] = {}
        for slot in availability:
            slot_data = TourDailyAvailabilityResponse(**slot)
            tour_key = (slot_data.tour_date, slot_data.tour_id)
            count_keys = set(slot_data.inventory_count.keys()) & set(
                slot_data.reservation_count.keys()
            )
            for count_key in count_keys:
                window = None
                if "_SECONDARY" in count_key:
                    window = slot_data.booking_windows.SECONDARY
                else:
                    window = slot_data.booking_windows.PRIMARY
                if (
                    not window
                    or now < window.open_timestamp
                    or now >= window.close_timestamp
                ):
                    continue
                inventory_count = slot_data.inventory_count[count_key]
                reservation_count = slot_data.reservation_count[count_key]
                if inventory_count <= reservation_count:
                    continue
                tour_data = availabilities.setdefault(tour_key, {"": slot_data})
                tour_data[slot_data.tour_time] = (
                    tour_data.get(slot_data.tour_time, 0)
                    + inventory_count
                    - reservation_count
                )
        for tour_date, tour_id in availabilities:
            tour_data = availabilities[tour_date, tour_id]
            slot_data = tour_data.pop("")
            fields = cls.make_campsite_availability_fields(
                tour_id,
                vars(slot_data),
                tour_date,
                campsite_metadata,
            )
            available_campsite = AvailableCampsite(
                campsite_occupancy=(1, sum(tour_data.values())),
                availability_status=slot_data.status,
                recreation_area=recreation_area,
                recreation_area_id=recreation_area_id,
                facility_name=facility_name,
                facility_id=facility_id,
                permitted_equipment=[
                    RecDotGovEquipment(
                        equipment_name=tour_time,
                        max_length=available_count,
                    )
                    for tour_time, available_count in tour_data.items()
                ],
                campsite_attributes=[],
                **fields,
            )
            total_campsite_availability.append(available_campsite)
        return total_campsite_availability


class RecreationDotGovTicket(RecreationDotGovTours):
    """
    RecreationDotGovTicket

    Tickets for Tours
    """

    facility_type = RIDBConfig.TICKET_FACILITY_FIELD_QUALIFIER
    api_search_fq = "entity_type:tour"
    api_base_path = "api/ticket/availability/facility/"
    booking_url = "https://www.recreation.gov/ticket/{facility_id}/ticket/{tour_id}"


class RecreationDotGovTimedEntry(RecreationDotGovTours):
    """
    RecreationDotGovTimedEntry

    Timed Entries
    """

    facility_type = RIDBConfig.TIMED_ENTRY_FACILITY_FIELD_QUALIFIER
    api_search_fq = "entity_type:timedentry_tour"
    api_base_path = "api/timedentry/availability/facility/"
    booking_url = (
        "https://www.recreation.gov/timed-entry/{facility_id}/ticket/{tour_id}"
    )


class RecreationDotGovDailyTicket(RecreationDotGovDailyMixin, RecreationDotGovTicket):
    """
    RecreationDotGovTicket: Daily

    Daily MixIn for Tickets
    """


class RecreationDotGovDailyTimedEntry(
    RecreationDotGovDailyMixin, RecreationDotGovTimedEntry
):
    """
    RecreationDotGovTimedEntry: Daily

    Daily MixIn for Tours
    """
