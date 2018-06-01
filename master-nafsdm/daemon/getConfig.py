# nafsdm-master daemon
# getConfig
# parses configuration file
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

import logging
from exitDaemon import *
import ConfigParser

class Config(object):
    import ConfigParser

    def __init__(self, configFile):
        parser = ConfigParser.ConfigParser()
        parser.read(configFile)

        try:
            self.type = parser.get("nafsdm_daemon", "type")
            self.check_interval = parser.get("nafsdm_daemon", "check_interval")
            self.master_bindPath = parser.get("nafsdm_daemon", "master_bindPath")
            self.master_hostname = parser.get("nafsdm_daemon", "master_hostname")
            self.master_abuseAddress = parser.get("nafsdm_daemon", "master_abuseAddress")


        except Exception:
            logging.exception("Could not read config. Please check if your config is setup properly.")
            logging.critical("Exiting due to previous error.")
            gracefulExit(1)

def getConfig():
    config = Config(configDir)

    return config
