""" myconfig.py v0.2
Handles reading/writing from config file
"""

import configparser

from mylog import get_logger

logger = get_logger("myconfig")

config = configparser.ConfigParser()

default_parameters = {
    "is_enabled": True,
    "zipcode": "97007",
    "country": "us",
    "ow_appid": None,
    "current_mode": 0,
    "mode1_color": (255, 0, 0),
    "mode3_color": (255, 0, 0),
    "mode4_color": (255, 0, 0),
    "mode6_color": (255, 0, 0),
    "mode7_color": (255, 0, 0),
    "mode9_index": 0,
}


def read_config_file(config=config, configfile="rcl-config.ini"):
    config.read(configfile)
    if len(config.sections()) == 0:
        logger.warning("Config file not found or improperly formatted.")
        return None
    return config


def load_configuration():
    config = read_config_file()
    if config is None:
        logger.warning("Config file not loaded.  Using default parameters.")
        return default_parameters
    parameters = {}
    for section in config.sections():
        for option in config.options(section):
            parameters[option] = process_option(section, option)
    validate_parameters(parameters)
    return parameters


def process_option(section, option):
    if "color" in str(option):
        val = config.get(section, option, fallback=(255, 0, 0))
        if val == "":
            val = (255, 0, 0)
        return eval(str(val))
    if ("current" in str(option)) or ("index" in str(option)):
        val = config.get(section, option, fallback=0)
        if val == "":
            val = 0
        return int(val)
    if str(option) == "is_enabled":
        val = config.getboolean(section, option, fallback=True)
        if val not in [True, False]:
            val = True
        return val
    if str(option) == "zipcode":
        return config.get(section, option, fallback=default_parameters["zipcode"])
    if str(option) == "country":
        return config.get(section, option, fallback=default_parameters["country"])
    return config.get(section, option, fallback=None)


def validate_parameters(p):
    for v_key in default_parameters.keys():
        if (v_key not in p.keys()) or (p[v_key] == ""):
            p[v_key] = default_parameters[v_key]
    return


def store_configuration(parameters, configfile="rcl-config.ini"):
    for key in parameters.keys():
        found = False
        for section in config.sections():
            if key in config.options(section):
                config[section][key] = str(parameters[key])
                found = True
                break
        if not found:
            config["other"][key] = str(parameters[key])
    with open(configfile, "w") as file:
        config.write(file)
    return
