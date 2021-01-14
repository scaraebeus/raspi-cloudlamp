""" myconfig.py v0.2
Handles reading/writing from config file
"""

import configparser

from mylog import get_logger

logger = get_logger("myconfig")

config = configparser.ConfigParser()

def load_config_file(configfile="rcl-config.ini"):
    config.read(configfile)
    if len(config.sections()) == 0:
        logger.warning("Config file not found or improperly formatted.")
    return config
