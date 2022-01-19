#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Camply Configuration Script
"""

from collections import OrderedDict
from datetime import datetime
import logging
from os.path import isfile
from time import sleep

from camply.config import FileConfig

logger = logging.getLogger(__name__)


def get_log_input(message: str):
    """
    Create a log message with a nice log format :)

    Parameters
    ----------
    message: str
        The message you'd like to print before getting input
    """
    datetime_string = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
    input_string = f"{datetime_string} [   INPUT]: {message} : "
    value = input(input_string)
    return value


def double_check(message: str) -> bool:
    """
    Double check if a step should be taken within CLI

    Parameters
    ----------
    message: str
        Message to log in interactive shell
    """
    operation_eval = True
    while operation_eval:
        first_confirmation = get_log_input(message=message)
        if first_confirmation.lower() == "y":
            second_confirmation = get_log_input("Are you sure? (y/n)")
            if second_confirmation.lower() != "y":
                logging.info("Okay, skipping")
                return False
            elif second_confirmation.lower() == "y":
                return True
        elif first_confirmation.lower() == "n":
            logging.info("Okay, skipping")
            return False
        else:
            logging.warning("Make sure to enter a 'y' or 'n'")
            operation_eval = True


def check_dot_camply_file() -> bool:
    """
    Check to see if the `.camply` file already exists

    Return the file existence status

    Returns
    -------
    bool
    """
    if isfile(FileConfig.DOT_CAMPLY_FILE) is True:
        logger.info("Skipping configuration. `.camply` file already exists: "
                    f"{FileConfig.DOT_CAMPLY_FILE}")
        return True
    else:
        return False


def generate_configuration() -> OrderedDict:
    """
    Generate the Camply Configuration Config

    Returns
    -------
    OrderedDict
        Dict of configuration values
    """
    config_dict = FileConfig.DOT_CAMPLY_FIELDS.copy()
    for field, field_dict in config_dict.items():
        default_value = field_dict["default"]
        field_note = field_dict['notes']
        if field_note is not None:
            logger.info(f"{field}: {field_note}")
        message = f"Enter value for `{field}`"
        if default_value != "":
            message += f" (default: `{default_value}`)"
        logged_input = get_log_input(message=message).strip()
        config_value = logged_input if logged_input != '' else default_value
        config_dict[field] = config_value
    return config_dict


def write_config_to_file(config_dict: OrderedDict) -> None:
    """
    Write the Configuration Object to a file

    Parameters
    ----------
    config_dict : OrderedDict
        Configuration Object
    """
    string_list = [
        "# CAMPLY CONFIGURATION FILE. ",
        "# SEE https://github.com/juftin/camply/blob/main/docs/examples/example.camply",
        ""
    ]
    for config_key, config_value in config_dict.items():
        string_list.append(f'{config_key}="{config_value}"')
    string_list.append("")
    with open(FileConfig.DOT_CAMPLY_FILE, "w") as file_object:
        file_object.write("\n".join(string_list))
        file_object.seek(0)


def generate_dot_camply_file():
    """
    Perform the larger Dot Camply File Generation
    """
    logger.info("Running camply configuration.")
    logger.info("This process generates a configuration file "
                "(https://github.com/juftin/camply/blob/main/example.camply)")
    logger.info("Do not include quotes around values")
    logger.info("To skip a configuration field or keep it as default, just press <Enter>.")
    sleep(1.5)
    if isfile(FileConfig.DOT_CAMPLY_FILE):
        logger.warning(f".camply file already exists on this machine: {FileConfig.DOT_CAMPLY_FILE}")
        overwrite = double_check("Would you like to overwrite your `.camply` "
                                 "configuration file? (y/n)")
        if overwrite is False:
            exit(0)
    config = generate_configuration()
    if double_check(f"Are you ready to publish this to a file at {FileConfig.DOT_CAMPLY_FILE}"):
        write_config_to_file(config_dict=config)
        logger.info(f"`.camply` file written to machine: {FileConfig.DOT_CAMPLY_FILE}")
