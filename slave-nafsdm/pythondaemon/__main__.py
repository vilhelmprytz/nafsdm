# nafsdm
# (c) Vilhelm Prytz 2018
# __main__
# get's stuff goooing
# https://github.com/mrkakisen/nafsdm

import logging
import sys
import shutil
import os
from daemon import *
from version import version
from getConfig import getConfig
from versionCheck import checkUpdate
from logPath import logPath

def main():
    # logger setup
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # format for logger
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # add stdout to logger
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # add file handler to logger
    fh = logging.FileHandler(logPath)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # welcome
    logging.info("*******************************************************")
    logging.info("Welcome to nafsdm-slave daemon - version " + version)
    logging.info("*******************************************************")

    logging.info("Running pre-start checks..")

    # check if the upgrade script is present (we shouldn't be running if so)
    if os.path.isfile("/home/slave-nafsdm/tempUpgrade/temp_upgrade.sh"):
        logging.warning("Upgrade script was found during pre-start checks. Please delete the upgrade script before runing nafsdm-slave!")
        logging.warning("Note: the script is left there because the config has changed and needs updating.")
        exit(1)

    if os.path.isfile("/home/slave-nafsdm/config-legacy.conf"):
        logging.warning("Legacy config was found. This probably means that nafsdm has been upgraded but the config hasn't been updated yet.")
        logging.warning("Remove the legacy config when finished.")
        exit(1)

    # check if the temp folder exists
    if os.path.isdir("/home/slave-nafsdm/temp"):
        logging.debug("Temp folder already exists.")
    else:
        if os.path.isfile("/home/slave-nafsdm/temp"):
            os.remove("/home/slave-nafsdm/temp")
            os.makedirs("/home/slave-nafsdm/temp")
        else:
            os.makedirs("/home/slave-nafsdm/temp")

    # get config
    config = getConfig()

    # check for updates
    checkUpdate(config, None)

    # run the daemon itself
    runDaemon(config)

if __name__ == "__main__":
    main()
    # graceful exit
    exit(0)
