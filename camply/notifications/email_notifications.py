"""
Push Notifications via Pushover
"""
import logging
from email.message import EmailMessage
from smtplib import SMTP_SSL
from typing import List

from camply.config import EmailConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class EmailNotifications(BaseNotifications):
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
        super().__init__()
        # PERFORM SOME VALIDATION
        if any(
            [
                EmailConfig.EMAIL_TO_ADDRESS in [None, ""],
                EmailConfig.EMAIL_USERNAME in [None, ""],
                EmailConfig.EMAIL_PASSWORD in [None, ""],
            ]
        ):
            variable_names = "\n\t".join(EmailConfig.ENVIRONMENT_VARIABLE_NAMES)
            optional_variable_names = "\n\t".join(
                EmailConfig.OPTIONAL_ENVIRONMENT_VARIABLE
            )
            error_message = (
                "Email Notification Auth Parameters not set. Run `camply configure` "
                f"or set the following Environment Variables:\n\t{variable_names}"
                "\nOptional Environment Variables:\n\t"
                f"{optional_variable_names}"
            )
            logger.error(error_message)
            raise EnvironmentError(error_message)
        # ATTEMPT AN EMAIL LOGIN AT INIT TO THROW ERRORS EARLY
        _email_server = SMTP_SSL(
            self.email_smtp_server,
            self.email_smtp_server_port,
        )
        _email_server.ehlo()
        _email_server.login(
            user=self.email_username,
            password=self._email_password,
        )
        _email_server.quit()

    def send_message(self, message: str, **kwargs) -> None:
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
        email["Subject"] = kwargs.get("subject", self.email_subject)
        email["From"] = kwargs.get("from", self.email_from)
        email["To"] = kwargs.get("to", self.email_to)
        email_server_user = kwargs.get("username", self.email_username)
        email_server_password = kwargs.get("password", self._email_password)
        email_server_smtp_server = kwargs.get("server", self.email_smtp_server)
        email_server_smtp_server_port = kwargs.get("port", self.email_smtp_server_port)
        email_server = SMTP_SSL(email_server_smtp_server, email_server_smtp_server_port)
        email_server.ehlo()
        email_server.login(user=email_server_user, password=email_server_password)
        logger.info(f"Sending Email to {email['To']}: {email['Subject']}")
        email_server.send_message(email)
        logger.info("Email sent successfully")
        email_server.quit()

    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs) -> None:
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        master_email_body_list = list()
        for campsite in campsites:
            message_title, formatted_dict = self.format_standard_campsites(
                campsite=campsite,
            )
            fields = [message_title]
            for key, value in formatted_dict.items():
                if key == "Permitted Equipment":
                    value = value.replace("\n  - ", "\n  \t  - ")
                fields.append(f"\t{key}: {value}")
            composed_message = "\n".join(fields) + "\n\n"
            master_email_body_list.append(composed_message)
        master_email_body = "\n".join(master_email_body_list)
        if len(campsites) > 0:
            self.send_message(message=master_email_body)
