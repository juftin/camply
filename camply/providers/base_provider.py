"""
BaseProvider Base Class
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union

import requests
import tenacity
from fake_useragent import UserAgent

from camply.config import SearchConfig
from camply.config.api_config import APIConfig
from camply.containers import CampgroundFacility

logger = logging.getLogger(__name__)


class ProviderError(Exception):
    """
    General Provider Error
    """


class ProviderSearchError(ProviderError):
    """
    Searching Error
    """


class BaseProvider(ABC):
    """
    Base Provider Class
    """

    RETRY_CONFIG: Type[APIConfig] = APIConfig
    FIVE_HUNDRED_STATUS_CODES = [
        # Official Server Errors
        500,  # Internal Server Error
        501,  # Not Implemented
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
        505,  # HTTP Version Not Supported
        506,  # Variant Also Negotiates
        507,  # Insufficient Storage
        508,  # Loop Detected
        510,  # Not Extended
        511,  # Network Authentication Required
        # Unofficial Server Errors
        509,  # Bandwidth Limit Exceeded
        529,  # Site is overloaded
        530,  # Site is frozen
        598,  # Network read timeout error
        599,  # Network connect timeout error
        # Vendor Errors
        520,  # Unknown Error
        521,  # Web Server Is Down
        522,  # Connection Timed Out
        523,  # Origin Is Unreachable
        524,  # A Timeout Occurred
        525,  # SSL Handshake Failed
        526,  # Invalid SSL Certificate
        527,  # Railgun Error
        530,  # Origin DNS Error
        561,  # Unauthorized
    ]

    def __repr__(self):
        """
        String Representation

        Returns
        -------
        str
        """
        return f"<{self.__class__.__name__}>"

    def __init__(self):
        """
        Initialize with a session
        """
        _user_agent = UserAgent(browsers=["chrome"]).random
        self.session = requests.Session()
        self.headers = {"User-Agent": _user_agent}
        self.session.headers = self.headers
        self.json_headers = self.headers.copy()
        self.json_headers.update({"Content-Type": "application/json"})

    @classmethod
    def get_search_months(cls, search_days) -> List[datetime]:
        """
        Get the Unique Months that need to be Searched

        Returns
        -------
        search_months: List[datetime]
            Datetime Months to search for reservations
        """
        truncated_months = {day.replace(day=1) for day in search_days}
        if len(truncated_months) > 1:
            logger.info(
                f"{len(truncated_months)} different months selected for search, "
                f"ranging from {min(search_days)} to {max(search_days)}"
            )
            return sorted(truncated_months)
        elif len(truncated_months) == 0:
            logger.error(SearchConfig.ERROR_MESSAGE)
            raise RuntimeError(SearchConfig.ERROR_MESSAGE)
        else:
            return sorted(truncated_months)

    @abstractmethod
    def find_campgrounds(self) -> List[CampgroundFacility]:
        """
        List Recreation Areas for the provider
        """

    def make_http_request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, Any]] = None,
        retry_response_codes: Optional[List[int]] = None,
    ) -> requests.Response:
        """
        Make an HTTP Request

        Parameters
        ----------
        url: str
            URL to make the request to
        method: str
            HTTP Method to use. Defaults to GET
        data: Optional[Union[Dict[str, Any], str]]
            Data to send with the request
        headers: Optional[Dict[str, Any]]
            Headers to send with the request
        retry_response_codes: Optional[List[int]]
            List of response codes to raise a ProviderError. on. Defaults to 500 range

        Returns
        -------
        response: requests.Response

        Raises
        ------
        ProviderError
            If the response code is in the retry_response_codes list
        HTTPError
            If the response code is not in the retry_response_codes list and the request fails
        """
        if retry_response_codes is None:
            retry_response_codes = self.FIVE_HUNDRED_STATUS_CODES
        response = self.session.request(
            method=method, url=url, data=data, headers=headers
        )
        if response.status_code not in retry_response_codes:
            response.raise_for_status()
        else:
            error_message = f"HTTP Error - {self.__class__.__name__} - {response.url} - {response.status_code}"
            logger.warning(error_message)
            error_message += f": {response.text}"
            raise ProviderError(error_message)
        return response

    def make_http_request_retry(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, Any]] = None,
        retry_response_codes: Optional[List[int]] = None,
    ) -> requests.Response:
        """
        Make an HTTP Request with Exponential Backoff

        This method will retry the request with exponential backoff if the request fails.
        By default, it will only ignore 500 range status codes, but this can be overridden.

        Parameters
        ----------
        url: str
            URL to make the request to
        method: str
            HTTP Method to use. Defaults to GET
        data: Optional[Union[Dict[str, Any], str]]
            Data to send with the request
        headers: Optional[Dict[str, Any]]
            Headers to send with the request
        retry_response_codes: Optional[List[int]]
            List of response codes to retry on. Defaults to 500 range

        Returns
        -------
        response: requests.Response
        """
        retryer = tenacity.Retrying(
            wait=tenacity.wait_random_exponential(
                multiplier=self.RETRY_CONFIG.RETRY_API_MULTIPLIER,
                max=self.RETRY_CONFIG.RETRY_MAX_API_ATTEMPTS,
            ),
            stop=tenacity.stop.stop_after_delay(
                self.RETRY_CONFIG.RETRY_MAX_API_TIMEOUT
            ),
            retry=tenacity.retry_if_exception_type(ProviderError),
        )
        response: requests.Response = retryer.__call__(
            fn=self.make_http_request,
            url=url,
            method=method,
            data=data,
            headers=headers,
            retry_response_codes=retry_response_codes,
        )
        return response
