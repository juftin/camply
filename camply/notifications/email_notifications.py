#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Push Notifications via Pushover
"""
from abc import ABC
from datetime import datetime
from email.message import EmailMessage
import logging
from smtplib import SMTP_SSL
from typing import List

from camply.config import CampsiteContainerFields, EmailConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class EmailNotifications(BaseNotifications, ABC):
    """
    Notifications via Email
    """

    email_subject = EmailConfig.EMAIL_SUBJECT_LINE
    email_from = EmailConfig.EMAIL_FROM_ADDRESS
    email_to = EmailConfig.EMAIL_TO_ADDRESS
    email_username = EmailConfig.EMAIL_USERNAME
    _email_password = EmailConfig.EMAIL_PASSWORD
    email_smtp_server = EmailConfig.EMAIL_SMTP_SERVER
    email_smtp_server_port = EmailConfig.EMAIL_SMTP_PORT

    def __init__(self):
        """
        Data Validation

        **kwargs
            Accepts: from, to, subject, username, password, server, port
        """
        # PERFORM SOME VALIDATION
        if any([EmailConfig.EMAIL_TO_ADDRESS in [None, ""],
                EmailConfig.EMAIL_USERNAME in [None, ""],
                EmailConfig.EMAIL_PASSWORD in [None, ""]]):
            variable_names = "\n\t".join(EmailConfig.ENVIRONMENT_VARIABLE_NAMES)
            optional_variable_names = "\n\t".join(
                EmailConfig.OPTIONAL_ENVIRONMENT_VARIABLE)
            error_message = ("Email Notification Auth Parameters not set. Run `camply configure` "
                             f"or set the following Environment Variables:\n\t{variable_names}"
                             "\nOptional Environment Variables:\n\t"
                             f"{optional_variable_names}")
            logger.error(error_message)
            raise EnvironmentError(error_message)
        # ATTEMPT AN EMAIL LOGIN AT INIT TO THROW ERRORS EARLY
        _email_server = SMTP_SSL(EmailNotifications.email_smtp_server,
                                 EmailNotifications.email_smtp_server_port)
        _email_server.ehlo()
        _email_server.login(user=EmailNotifications.email_username,
                            password=EmailNotifications._email_password)
        _email_server.quit()

    def __repr__(self):
        """
        String Representation
        """
        return "<EmailNotifications>"

    @staticmethod
    def send_message(message: str, **kwargs) -> object:
        """
        Send a message via Email

        Parameters
        ----------
        message: str
            Email Body
        **kwargs
            Accepts: from, to, subject, username, password, server, port

        Returns
        -------
        object
        """
        email = EmailMessage()
        email.set_content(message)
        email["Subject"] = kwargs.get("subject", EmailNotifications.email_subject)
        email["From"] = kwargs.get("from", EmailNotifications.email_from)
        email["To"] = kwargs.get("to", EmailNotifications.email_to)
        email_server_user = kwargs.get("username", EmailNotifications.email_username)
        email_server_password = kwargs.get("password",
                                           EmailNotifications._email_password)
        email_server_smtp_server = kwargs.get("server",
                                              EmailNotifications.email_smtp_server)
        email_server_smtp_server_port = kwargs.get("port",
                                                   EmailNotifications.email_smtp_server_port)
        email_server = SMTP_SSL(email_server_smtp_server,
                                email_server_smtp_server_port)
        email_server.ehlo()
        email_server.login(user=email_server_user,
                           password=email_server_password)
        logger.info(f"Sending Email to {email['To']}: {email['Subject']}")
        response = email_server.send_message(email)
        logger.info("Email sent successfully")
        email_server.quit()
        return response

    @staticmethod
    def send_campsites(campsites: List[AvailableCampsite], **kwargs) -> None:
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        master_email_body_list = list()
        for campsite in campsites:
            fields = list()
            message_title = (
                f"{campsite.recreation_area} | {campsite.facility_name} | "
                f"{campsite.booking_date.strftime('%Y-%m-%d')}:")
            fields.append(message_title)
            for key, value in campsite._asdict().items():
                if key in [CampsiteContainerFields.BOOKING_DATE,
                           CampsiteContainerFields.BOOKING_END_DATE]:
                    value: datetime = value.strftime("%Y-%m-%d")
                elif key == CampsiteContainerFields.BOOKING_URL:
                    key = "booking_link"
                formatted_key = key.replace("_", " ").title()
                fields.append(f"\t{formatted_key}: {value}")
            composed_message = "\n".join(fields) + "\n\n"
            master_email_body_list.append(composed_message)
        master_email_body = "\n".join(master_email_body_list)
        if len(campsites) > 0:
            EmailNotifications.send_message(message=master_email_body)
