"""
Recreation.gov Provider Configuration
"""

from datetime import timedelta
from urllib.parse import urljoin

from pydantic import BaseModel, Field


class RecreationGovConfig(BaseModel):
    """
    Configuration parameters and URLs for Recreation.gov.
    """

    api_scheme: str = "https"
    api_netloc: str = "www.recreation.gov"

    # Base URLs
    base_url: str = "https://www.recreation.gov/"
    ridb_base_url: str = "https://ridb.recreation.gov/"

    # Referer Header Value
    referer_header: str = "https://www.recreation.gov/"

    # API and Web Endpoints/Prefixes
    campsite_search_endpoint: str = "api/search/campsites"
    campsite_availability_endpoint: str = "api/camps/availability/campground"
    ridb_export_endpoint: str = "downloads/RIDBFullExport_V1_JSON.zip"
    gateway_endpoint_prefix: str = "gateways"
    campground_endpoint_prefix: str = "camping/campgrounds"

    # Date formatting pattern for API month queries
    api_month_format: str = "%Y-%m-01T00:00:00.000Z"

    # Expiration time for offline cached data
    offline_cache_expiration: timedelta = Field(
        default_factory=lambda: timedelta(hours=12)
    )

    @property
    def campsite_search_url(self) -> str:
        """
        Full campsite search metadata URL.
        """
        return urljoin(self.base_url, self.campsite_search_endpoint)

    @property
    def campsite_availability_url(self) -> str:
        """
        Full campsite availability URL prefix.
        """
        return urljoin(self.base_url, self.campsite_availability_endpoint)

    @property
    def ridb_export_url(self) -> str:
        """
        Full RIDB export data download URL.
        """
        return urljoin(self.ridb_base_url, self.ridb_export_endpoint)

    @property
    def gateway_url_prefix(self) -> str:
        """
        Full gateway URL prefix.
        """
        return urljoin(self.base_url, self.gateway_endpoint_prefix)

    @property
    def campground_url_prefix(self) -> str:
        """
        Full campground URL prefix.
        """
        return urljoin(self.base_url, self.campground_endpoint_prefix)
