# nafsdm
# (c) Vilhelm Prytz 2017
# getConfig
# parses the config and returns in var

import logging
from configDir import __configDir__ as configDir
import ConfigParser

class Config(object):
    import ConfigParser

    def __init__(self, configFile):
        parser = ConfigParser.ConfigParser()
        parser.read(configFile)

        try:
            self.host = parser.get("nafsdm", "host")
            self.user = parser.get("nafsdm", "user")
            self.update_interval = parser.get("nafsdm", "update_interval")
            self.type = parser.get("nafsdm", "type")
            self.bindPath = parser.get("nafsdm", "bindPath")
            self.nodeName = parser.get("nafsdm", "nodeName")

        except Exception:
            logging.exception("Could not read config. Please check your config if it's setup properly.")
            logging.critical("Exiting application due to recent error.")
            quit(1)


def getConfig():
    config = Config(configDir)

    return config
