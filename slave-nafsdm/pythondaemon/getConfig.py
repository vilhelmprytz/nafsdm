# nafsdm
# getConfig
# parses the config and returns in var

from daemonlog import *
from configDir import __configDir__ as configDir
import ConfigParser

def getConfig():
    parser = ConfigParser.ConfigParser()
    parser.read(configDir)
    try:
        config = []
        config.append(parser.get("dnsman", "host")) # 0
        config.append(parser.get("dnsman", "user")) # 1
        config.append(parser.get("dnsman", "update_interval")) # 2
        config.append(parser.get("dnsman", "type")) # 3
        config.append(parser.get("dnsman", "bindPath")) # 4
        config.append(parser.get("dnsman", "nodeName")) # 5

        return config
    except ConfigParser.MissingSectionHeaderError or ConfigParser.ParsingError:
        log("FATAL: Could not read config. Please check your config if it's setup properly.")
        quit(1)
