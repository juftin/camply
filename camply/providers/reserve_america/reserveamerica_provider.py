"""
Reserve America Web Searching Utilities
"""

import logging
from abc import ABC
from datetime import date, datetime
from typing import List, Optional, Union

from scrapy.crawler import CrawlerProcess

# TODO: Update ReserveAmericaConfig as needed
# TODO: Add and create other classes as needed
from camply.containers import CampgroundFacility
from camply.containers.data_containers import AvailableCampsite
from camply.providers.base_provider import BaseProvider
from camply.providers.reserve_america.reserve_america_scraper.spiders.campground_spider import (
    CampgroundSpider,
)
from camply.utils.general_utils import make_list

logger = logging.getLogger(__name__)

scrapy_base_settings = {
    "BOT_NAME": "reserve_america_scraper",
    "ROBOTSTXT_OBEY": False,
    "CONCURRENT_REQUESTS": 1,
    "DOWNLOAD_DELAY": 1,
    "DOWNLOADER_MIDDLEWARES": {
        "camply.providers.reserve_america.reserve_america_scraper.middlewares.HumanInTheDownloaderMiddleware": 543,
    },
}


class ReserveAmerica(BaseProvider, ABC):
    """
    Python Class for Reserve America Web Searching
    """

    def __init__(self):
        """
        Initialize the ReserveAmericaBase class.
        """
        super().__init__()
        # TODO: Initialize session/cookies

    # TODO return availability, see search_reserveamerica.py for more details

    def find_campgrounds(
        self,
        park_ids: Optional[List[str]] = None,
    ) -> List[CampgroundFacility]:
        """
        Get Campground metadata from ReserveAmerica

        Parameters
        ----------
        park_ids: Optional[List[str]]
            ReserveAmerica Park ID or List of IDs

        Returns
        -------
        List[CampgroundFacility]
            List of CampgroundFacility objects
        """

        found_campgrounds: List[CampgroundFacility] = []
        logger.debug(f"Finding campgrounds for park IDs: {park_ids}")
        for park_id in make_list(park_ids):
            campground = CampgroundFacility(
                facility_name="Placeholder Facility Name",
                # TODO: Replace with actual name
                facility_id=park_id,
                recreation_area="Placeholder Recreation Area",
                recreation_area_id=park_id,
                # TODO: Replace with actual recreation area ID
            )
            found_campgrounds.append(campground)
        logger.debug(
            f"Found {len(found_campgrounds)} campgrounds for park IDs: {park_ids}"
        )
        return found_campgrounds

    def get_campsites(
        self,
        park_id: int,
        start_date: Union[datetime, date],
        end_date: Union[datetime, date],
        **spider_args,
    ) -> List[AvailableCampsite]:
        """
        Run the CampgroundSpider to scrape campground data,
        returning a list of `AvailableCampsite`.
        """

        start_date_str = start_date.strftime("%m/%d/%Y")
        end_date_str = end_date.strftime("%m/%d/%Y")

        scrapy_settings = scrapy_base_settings.copy()
        scrapy_settings.update(
            [
                (
                    "SPIDER_MIDDLEWARES",
                    {
                        "camply.providers.reserve_america.reserve_america_scraper.middlewares.CamplyReserveAmericaSpiderMiddleware": 543,
                    },
                ),
            ]
        )

        # Create a CrawlerProcess using your project settings
        process = CrawlerProcess(settings=scrapy_settings)

        # Run the spider
        crawler = process.create_crawler(CampgroundSpider)
        process.crawl(
            crawler,
            park_id=park_id,
            start_date=start_date_str,
            end_date=end_date_str,
            **spider_args,
        )

        process.start()  # Blocks until crawl is finished

        # Retrieve the accumulated results from the spider (populated by your new middleware)
        scraped_campsites = getattr(crawler.spider, "available_campsites", [])

        return scraped_campsites
