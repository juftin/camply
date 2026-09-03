"""
Recreation.gov Web Searching Utilities
"""

import heapq
import logging
import os
import time
from abc import ABC
from datetime import datetime
from random import uniform
from time import sleep
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import tenacity

from camply.config import RecreationBookingConfig
from camply.config.search_config import EquipmentConfig, EquipmentOptions
from camply.containers import AvailableCampsite, CampgroundFacility, SearchWindow
from camply.containers.api_responses import RecDotGovCampsite, RecDotGovSearchResult
from camply.containers.data_containers import ListedCampsite
from camply.exceptions import SearchError
from camply.providers import (
    RecreationDotGov,
    RecreationDotGovDailyTicket,
    RecreationDotGovDailyTimedEntry,
    RecreationDotGovTicket,
    RecreationDotGovTimedEntry,
)
from camply.notifications.multi_provider_notifications import MultiNotifierProvider
from camply.search.base_search import BaseCampingSearch
from camply.utils import logging_utils, make_list

logger = logging.getLogger(__name__)


class SearchRecreationDotGovBase(BaseCampingSearch, ABC):
    """
    Camping Search Object
    """

    accepted_equipment: Optional[
        List[str]
    ] = EquipmentOptions.__all_accepted_equipment__

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
        super(SearchRecreationDotGovBase, self).__init__(
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
            offline_search=offline_search,
            offline_search_path=offline_search_path,
            **kwargs,
        )
        self.campsite_finder: RecreationDotGov
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
        searchable_campgrounds: List[CampgroundFacility]
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
                    cls.accepted_equipment
                    == EquipmentOptions.__all_accepted_equipment__
                    and equipment_name.lower() not in cls.accepted_equipment
                ):
                    logger.warning(
                        f"Equipment name not recognized: {equipment_name}. This won't "
                        "be used for filtering. "
                        "Acceptable options are: "
                        f"{', '.join(cls.accepted_equipment)}"
                    )
                elif (
                    cls.accepted_equipment == EquipmentConfig.TIMESTAMP_EQUIPMENT
                    and equipment_name not in EquipmentConfig.TIMESTAMP_EQUIPMENT
                ):
                    logger.warning(
                        'Invalid Timestamp supplied, "%s". This won\'t be used for filtering',
                        equipment_name,
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
        Return a List of Campgrounds to search when provided with Campground IDs

        Returns
        -------
        facilities: List[CampgroundFacility]
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
        facilities: List[CampgroundFacility]
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
        facilities: List[CampgroundFacility]
            List of searchable campground IDs
        """
        facilities = []
        for rec_area in self._recreation_area_id:
            campground_array = self.campsite_finder.find_facilities_per_recreation_area(
                rec_area_id=rec_area
            )
            facilities += campground_array
        return facilities

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return All Monthly Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        found_campsites = []
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
                logger.info(
                    f"\t{logging_utils.get_emoji(campsites)}\t"
                    f"{len(campsites)} total sites found in month of "
                    f"{month.strftime('%B')}"
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
        return self._filter_and_consolidate_campsites(found_campsites)

    def _filter_and_consolidate_campsites(
        self, campsites: List[AvailableCampsite]
    ) -> List[AvailableCampsite]:
        """
        Consolidate raw campsites through date overlap, minimum nights, and equipment filters.
        """
        if not campsites:
            return []
        campsite_df = self.campsites_to_df(campsites=campsites)
        campsite_df_validated = self._filter_date_overlap(campsites=campsite_df)
        compiled_campsite_df = self._consolidate_campsites(
            campsite_df=campsite_df_validated, nights=self.nights
        )
        equipment_filtered_campsites = self.filter_campsites_to_equipment(
            campsites=compiled_campsite_df
        )
        return self.df_to_campsites(campsite_df=equipment_filtered_campsites)

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
            columns=[*column_names, "equipment_name", "max_length"],
        )
        if self.accepted_equipment == EquipmentOptions.__all_accepted_equipment__:
            joined_data["equipment_name_normalized"] = (
                joined_data["equipment_name"]
                .fillna("")
                .apply(lambda x: EquipmentConfig.EQUIPMENT_REVERSE_MAPPING[x])
            )
        else:
            joined_data["equipment_name_normalized"] = joined_data["equipment_name"]
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

    def _get_listable_campsites(
        self, campsites: Union[List[RecDotGovCampsite], List[RecDotGovSearchResult]]
    ) -> List[ListedCampsite]:
        """
        Get Listable Campsites

        Returns
        -------
        List[ListedCampsite]
        """
        if isinstance(campsites[0], RecDotGovCampsite):
            return [
                ListedCampsite(
                    id=item.campsite_id,
                    facility_id=item.asset_id,
                    name=item.name,
                )
                for item in campsites
            ]
        elif isinstance(campsites[0], RecDotGovSearchResult):
            return [
                ListedCampsite(
                    id=item.entity_id,
                    facility_id=item.parent_id,
                    name=item.name,
                )
                for item in campsites
            ]
        else:
            raise NotImplementedError(
                f"Cannot get listable campsites from type {type(campsites[0])}"
            )

    def list_campsite_units(self) -> List[ListedCampsite]:
        """
        List Campsite Units

        Returns
        -------
        List[ListedCampsite]
        """
        recdotgov_campsites = self.campsite_finder.get_internal_campsites(
            facility_ids=[item.facility_id for item in self.campgrounds]
        )
        listable_campsites = self._get_listable_campsites(campsites=recdotgov_campsites)
        self.log_listed_campsites(
            campsites=listable_campsites,
            facilities=self.campgrounds,
        )
        return listable_campsites


class SearchRecreationDotGov(SearchRecreationDotGovBase):
    """
    Searches on Recreation.gov for Campsites (default provider)
    """

    provider_class = RecreationDotGov

    @staticmethod
    def _log_staleness_report(
        window_stats: Dict[int, Dict[str, Any]],
        window_duration_seconds: float,
        previous_window_avg_age: Optional[float] = None,
        rate_limits: int = 0,
    ) -> float:
        """
        Log periodic recency and staleness report per campground.
        """
        lines = [
            "================================================================================",
            f"📊 [5-Minute Recency & Staleness Report] (Duration: {window_duration_seconds / 60:.1f}m)",
            "--------------------------------------------------------------------------------",
        ]
        total_queries = 0
        all_ages: List[int] = []
        total_fresh = 0
        total_cache = 0

        for facil_id, s in window_stats.items():
            name = s["name"]
            queries = s["queries"]
            total_queries += queries
            if queries == 0:
                lines.append(f"{name} ({facil_id}): No queries recorded in this window.")
                continue

            ages = s["ages"]
            all_ages.extend(ages)
            fresh = s["fresh_hits"]
            cache = s["cache_hits"]
            total_fresh += fresh
            total_cache += cache

            avg_age = sum(ages) / len(ages)
            min_age = min(ages)
            max_age = max(ages)
            fresh_pct = (fresh / queries) * 100.0
            ultra_fresh = sum(1 for a in ages if a <= 2)
            ultra_fresh_pct = (ultra_fresh / queries) * 100.0
            avg_lat = sum(s["latencies"]) / len(s["latencies"]) if s["latencies"] else 0.0

            lines.append(f"{name} ({facil_id}):")
            lines.append(
                f"  • Queries: {queries} | Fresh Origin: {fresh} ({fresh_pct:.1f}%) | Cache Hits: {cache}"
            )
            lines.append(
                f"  • Staleness (Age): avg {avg_age:.1f}s [min: {min_age}s, max: {max_age}s] | <=2s: {ultra_fresh_pct:.1f}%"
            )
            lines.append(f"  • Avg Latency: {avg_lat:.1f}ms")

        lines.append("--------------------------------------------------------------------------------")
        duration_minutes = window_duration_seconds / 60.0
        req_per_min = (total_queries / duration_minutes) if duration_minutes > 0 else 0.0
        overall_avg_age = (sum(all_ages) / len(all_ages)) if all_ages else 0.0
        overall_fresh_pct = (total_fresh / total_queries * 100.0) if total_queries > 0 else 0.0

        if overall_avg_age <= 3.5:
            drift_status = "STABLE 🟢 (Optimal cache edge sniping)"
        elif overall_avg_age <= 6.0:
            drift_status = "STEADY 🟢 (Good cache recency)"
        elif overall_avg_age <= 9.0:
            drift_status = "EVALUATING 🟡 (Moderate cache age)"
        else:
            drift_status = "DRIFTED 🔴 (Stale cache hits elevated)"

        if previous_window_avg_age is not None:
            diff = overall_avg_age - previous_window_avg_age
            if abs(diff) < 0.3:
                trend_str = f"±0.0s (Steady ↔, prev window: {previous_window_avg_age:.1f}s)"
            elif diff < 0:
                trend_str = f"{diff:.1f}s (Fresher ↗, prev window: {previous_window_avg_age:.1f}s)"
            else:
                trend_str = f"+{diff:.1f}s (Aging ↘, prev window: {previous_window_avg_age:.1f}s)"
        else:
            trend_str = "Baseline window"

        waf_budget_str = f"{total_queries}/100"

        lines.append("Summary Across Campgrounds:")
        lines.append(
            f"  • Total Queries: {total_queries} ({req_per_min:.1f} req/min | 5-min WAF usage: {waf_budget_str})"
        )
        lines.append(
            f"  • Overall Avg Staleness: {overall_avg_age:.1f}s | Fresh Origin Ratio: {overall_fresh_pct:.1f}%"
        )
        lines.append(f"  • Rate Limits (429): {rate_limits}")
        lines.append(f"  • Drift Trend: {trend_str} | Status: {drift_status}")
        lines.append("================================================================================")

        logger.info("\n" + "\n".join(lines))
        return overall_avg_age

    def _search_campsites_continuous(
        self,
        log: bool = True,
        verbose: bool = False,
        polling_interval: Optional[int] = None,
        notification_provider: str = "silent",
        notify_first_try: bool = False,
        search_forever: bool = False,
        search_once: bool = False,
    ) -> List[AvailableCampsite]:
        """
        Continuously Search SFO CloudFront POP Adaptively Aligned to Cache Boundaries
        """
        if len(self.campgrounds) == 0:
            error_message = "No campgrounds found to search"
            logger.error(error_message)
            raise SearchError(error_message)

        if self.campsite_metadata is None:
            self.campsite_metadata = (
                self.campsite_finder.get_internal_campsite_metadata(
                    facility_ids=[facil.facility_id for facil in self.campgrounds]
                )
            )
            logger.info(
                "Metadata fetched for %s campsites across %s campgrounds",
                len(self.campsite_metadata),
                len(self.campgrounds),
            )

        if search_once is True:
            return super()._search_campsites_continuous(
                log=log,
                verbose=verbose,
                polling_interval=polling_interval,
                notification_provider=notification_provider,
                notify_first_try=notify_first_try,
                search_forever=search_forever,
                search_once=search_once,
            )

        logger.info(
            "Initializing Adaptive SFO Edge Cache Sniper "
            f"across {len(self.campgrounds)} campground(s)..."
        )
        if self.notifier is None:
            self.notifier = MultiNotifierProvider(provider=notification_provider)
        self.notifier.log_providers()

        # Strict Global Pacing Floor:
        # For 3 campgrounds and 15s cache TTL, ~4.8s spacing provides ideal cache alignment
        # (15s / 3 = 5.0s) while capping request velocity at 12.5 req/min (<= 62.5 req / 5 min),
        # providing a 37% safety buffer below AWS WAF / origin rate ceilings.
        min_request_spacing = 4.8

        # Build Priority Queue for Campgrounds
        # Event item: (next_poll_time, campground, month, event_id)
        pq = []
        event_counter = 0

        # Stagger initial checks by 5.0s with a 2s startup breather after metadata fetching
        initial_stagger = time.time() + 2.0
        for campground in self.campgrounds:
            for month in self.search_months:
                heapq.heappush(
                    pq,
                    (initial_stagger, campground, month, event_counter),
                )
                initial_stagger += 5.0
                event_counter += 1

        continuous_search_attempts = 1
        retryer = tenacity.Retrying()
        last_request_time = 0.0
        last_ages: Dict[Tuple[int, str], int] = {}  # Tracks (campground_id, month_str) -> last observed age

        # Recency & Staleness Monitoring: logs per-campground stats every 5 minutes (300s)
        def _init_window_stats() -> Dict[int, Dict[str, Any]]:
            return {
                c.facility_id: {
                    "name": c.facility_name,
                    "queries": 0,
                    "ages": [],
                    "latencies": [],
                    "fresh_hits": 0,
                    "cache_hits": 0,
                }
                for c in self.campgrounds
            }

        window_stats = _init_window_stats()
        window_start_time = time.time()
        last_stats_report_time = time.time()
        stats_interval = float(os.getenv("CAMPLY_STALENESS_REPORT_INTERVAL", "300"))
        previous_window_avg_age: Optional[float] = None
        window_rate_limits = 0

        while True:
            next_poll_time, campground, month, event_id = heapq.heappop(pq)
            sleep_needed = next_poll_time - time.time()
            if sleep_needed > 0:
                time.sleep(sleep_needed)

            # Enforce global pacing floor to prevent bursts and stay strictly within WAF limits
            time_since_last = time.time() - last_request_time
            if time_since_last < min_request_spacing:
                time.sleep(min_request_spacing - time_since_last)
            last_request_time = time.time()

            try:
                # Query local Bay Area SFO POP (~19ms RTT)
                availabilities, meta = self.campsite_finder.get_recdotgov_availability(
                    campground_id=campground.facility_id,
                    month=month,
                )
                age = meta["age"]
                cf_pop = meta["cf_pop"]
                x_cache = meta["x_cache"]
                latency_ms = meta["latency_ms"]

                # Record metrics for 5-minute recency & staleness report
                c_stats = window_stats.setdefault(
                    campground.facility_id,
                    {
                        "name": campground.facility_name,
                        "queries": 0,
                        "ages": [],
                        "latencies": [],
                        "fresh_hits": 0,
                        "cache_hits": 0,
                    },
                )
                c_stats["queries"] += 1
                c_stats["ages"].append(age)
                c_stats["latencies"].append(latency_ms)
                if "Miss" in x_cache or age == 0:
                    c_stats["fresh_hits"] += 1
                else:
                    c_stats["cache_hits"] += 1

                key = (campground.facility_id, month.strftime("%Y-%m"))
                prev_age = last_ages.get(key, -1)
                last_ages[key] = age

                # Adaptive SFO Cache Expiration Timing
                if "Miss" in x_cache or age == 0:
                    # Fresh origin fetch! SFO cache expires in 15.0s. Check right after eviction.
                    remaining_ttl = 15.3
                elif age >= 14:
                    if prev_age >= 14:
                        # Cache has not evicted yet after probe; back off 6.0s to avoid tight loop
                        remaining_ttl = 6.0
                    else:
                        # Near eviction; check in 2.0s to catch the fresh origin cycle
                        remaining_ttl = 2.0
                else:
                    # External caller refreshed cache `age` seconds ago. It expires in (15.0 - age) seconds.
                    remaining_ttl = max(3.0, (15.0 - age) + 0.3)

                cache_indicator = (
                    "⚡ [FRESH ORIGIN]"
                    if "Miss" in x_cache or age == 0
                    else f"[Age: {age}s]"
                )
                logger.info(
                    f"[Cache Recency] {cf_pop:<10} (SFO) | "
                    f"{campground.facility_name} ({campground.facility_id}): "
                    f"{x_cache} {cache_indicator} | RTT: {latency_ms:.1f}ms | "
                    f"Next check in {remaining_ttl:.1f}s"
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

                matching_campsites = self._filter_and_consolidate_campsites(campsites)
                found_set = set(matching_campsites)
                new_campsites = found_set.difference(self.campsites_found)

                if new_campsites:
                    logger.info(
                        f"🎉 [MATCH FOUND] {len(new_campsites)} available site(s) discovered in "
                        f"{campground.facility_name} via {cf_pop} (SFO)!"
                    )
                    self.assemble_availabilities(
                        matching_data=list(new_campsites), log=log, verbose=verbose
                    )
                    self.campsites_found.update(new_campsites)
                    self._handle_notifications(
                        retryer=retryer,
                        notifier=self.notifier,
                        logged_campsites=list(new_campsites),
                        continuous_search_attempts=continuous_search_attempts,
                        notify_first_try=notify_first_try,
                    )
                    if search_forever is False:
                        logger.info("Campsites found and search_forever=False. Exiting search.")
                        return list(self.campsites_found)

                next_poll = time.time() + remaining_ttl
                heapq.heappush(
                    pq,
                    (next_poll, campground, month, event_id),
                )
                continuous_search_attempts += 1

            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    window_rate_limits += 1
                    logger.warning(
                        "⚠️ [RATE LIMIT] CloudFront HTTP 429 detected! Pausing all requests for 75 seconds to let WAF block expire..."
                    )
                    time.sleep(75.0)
                    now = time.time()
                    pq = [(now + idx * 5.0, c, m, eid) for idx, (t, c, m, eid) in enumerate(pq)]
                    heapq.heapify(pq)
                    last_request_time = time.time()
                    continue

                logger.warning(
                    f"Error polling {campground.facility_name} via SFO: {e}. Retrying in 5.0s..."
                )
                heapq.heappush(
                    pq,
                    (time.time() + 5.0, campground, month, event_id),
                )

            # Periodic 5-minute Recency & Staleness Report
            now = time.time()
            if now - last_stats_report_time >= stats_interval:
                previous_window_avg_age = self._log_staleness_report(
                    window_stats=window_stats,
                    window_duration_seconds=now - window_start_time,
                    previous_window_avg_age=previous_window_avg_age,
                    rate_limits=window_rate_limits,
                )
                window_stats = _init_window_stats()
                window_start_time = now
                last_stats_report_time = now
                window_rate_limits = 0


class SearchRecreationDotGovDailyTicket(SearchRecreationDotGovBase):
    """
    Searches on Recreation.gov for Tickets and Tours (Daily)
    """

    provider_class = RecreationDotGovDailyTicket
    accepted_equipment = EquipmentConfig.TIMESTAMP_EQUIPMENT


class SearchRecreationDotGovDailyTimedEntry(SearchRecreationDotGovBase):
    """
    Searches on Recreation.gov for Timed Entries (Daily)
    """

    provider_class = RecreationDotGovDailyTimedEntry
    accepted_equipment = EquipmentConfig.TIMESTAMP_EQUIPMENT


class SearchRecreationDotGovTicket(SearchRecreationDotGovBase):
    """
    Searches on Recreation.gov for Tickets and Tours
    """

    provider_class = RecreationDotGovTicket


class SearchRecreationDotGovTimedEntry(SearchRecreationDotGovBase):
    """
    Searches on Recreation.gov for Timed Entries
    """

    provider_class = RecreationDotGovTimedEntry
