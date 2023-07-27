"""
Push Notifications via Discord
"""

import logging
from typing import List

import requests

from camply.config import DiscordConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class DiscordNotifications(BaseNotifications):
    """
    Push Notifications via Discord
    """

    def __init__(self):
        super().__init__()
        self.session.headers.update({"Content-Type": "application/json"})
        if any([DiscordConfig.DISCORD_WEBHOOK is None, DiscordConfig.DISCORD_WEBHOOK == ""]):
            warning_message = (
                "Discord is not configured properly. To send Discord messages "
                "make sure to run `camply configure` or set the "
                "proper environment variable: `DISCORD_WEBHOOK`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def send_message(self, message: str, **kwargs) -> requests.Response:
        """
        Send a message via Discord - if environment variables are configured.

        Parameters
        ----------
        message: str

        Returns
        -------
        requests.Response
        """
        message_json = kwargs
        if message:
            message_json["content"] = message

        logger.debug(message_json)
        response = self.session.post(
            url=DiscordConfig.DISCORD_WEBHOOK,
            json=message_json,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as he:
            logger.warning(
                "Notifications weren't able to be sent to Discord. "
                "Your configuration might be incorrect."
            )
            raise ConnectionError(response.text) from he
        return response

    def block_for_campsite(self, campsite: AvailableCampsite):
        message_title, formatted_dict = self.format_standard_campsites(
            campsite=campsite,
        )

        # Remove items that will be templated as part of the embed.
        del formatted_dict["Recreation Area"]
        del formatted_dict["Booking Date"]
        del formatted_dict["Booking End Date"]
        del formatted_dict["Facility Name"]
        del formatted_dict["Booking Link"]
        del formatted_dict["Campsite Site Name"]
        del formatted_dict["Campsite Loop Name"]
        del formatted_dict["Recreation Area Id"]
        del formatted_dict["Facility Id"]
        del formatted_dict["Campsite Id"]

        return {
            "author": {
                "name": f"🏕 {campsite.recreation_area}"
            },
            "title": f"{campsite.facility_name} {campsite.campsite_loop_name} #{campsite.campsite_site_name}",
            "description": f"{campsite.booking_date:%Y/%m/%d} to {campsite.booking_end_date:%Y/%m/%d}",
            "url": campsite.booking_url,
            "color": 2375436,
            "fields": [
                {
                    "name": key,
                    "value": str(value)
                } for key, value in formatted_dict.items()
            ],
            "footer": {
                "text": "camply, the campsite finder ⛺️"
            }
        }

    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: AvailableCampsite
        """
        if campsites:
            self.send_message(
                message="",
                embeds=[self.block_for_campsite(campsite) for campsite in campsites],
            )
