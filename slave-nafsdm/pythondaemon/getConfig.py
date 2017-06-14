# nafsdm
# getConfig
# parses the config and returns in var

from daemonlog import *
from configDir import __configDir__ as configDir
import ConfigParser

class Config(object):
    import ConfigParser

    def __init__(self, configFile):
        parser = ConfigParser.ConfigParser()
        parser.read(configFile)

        try:
            self.host = parser.get("dnsman", "host")
            self.user = parser.get("dnsman", "user")
            self.update_interval = parser.get("dnsman", "update_interval")
            self.type = parser.get("dnsman", "type")
            self.bindPath = parser.get("dnsman", "bindPath")
            self.nodeName = parser.get("dnsman", "nodeName")

        except ConfigParser.MissingSectionHeaderError or ConfigParser.ParsingError:
            log("FATAL: Could not read config. Please check your config if it's setup properly.")
            quit(1)


def getConfig():
    config = Config(configDir)

    return config
