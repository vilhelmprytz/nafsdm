# nafsdm
# (c) Vilhelm Prytz 2017
# getConfig
# parses the config and returns in var
# https://github.com/mrkakisen/nafsdm

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

            # options section
            self.options_upgradeOnStart = parser.get("options", "upgradeOnStart")

            # dev section
            self.dev_github_branch = parser.get("development", "github_branch")
            self.dev_skipVersionCheck = parser.get("development", "skipVersionCheck")
            self.dev_incrementalCommitVersions = parser.get("development", "incrementalCommitVersions")

        except Exception:
            logging.exception("Could not read config. Please check if your config is setup properly.")
            logging.critical("Exiting due to previous error.")
            quit(1)


def getConfig():
    config = Config(configDir)

    return config
