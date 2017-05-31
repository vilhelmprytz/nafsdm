# dns-manager
# getConfig
# parses the config and returns in var

from daemonlog import *
from configDir import __configDir__ as configDir

def getConfig():
    parser = ConfigParser.ConfigParser()
    parser.read(configDir)
    try:
        config = []
        config.append(parser.get("dnsman", "host")) # 0
        config.append(parser.get("dnsman", "user")) # 1
        config.append(parser.get("dnsman", "update_interval")) # 2

        return config
    except ConfigParser.MissingSectionHeaderError or ConfigParser.ParsingError:
        log("FATAL: Could not read config. Please check your config if it's setup properly.")
        quit(0)
