# nafsdm
# (c) Vilhelm Prytz 2017
# __main__
# get's stuff goooing

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
    logging.info("Welcome to Slave nafsdm version " + version)

    # check if the upgrade script is present (we shouldn't be running if so)
    if os.path.isfile("/home/slave-nafsdm/tempUpgrade/temp_upgrade.sh"):
        logging.warning("Upgrade script found. Please delete the upgrade script before runing nafsdm-slave!")
        logging.warning("Note: the script is left there because the config has changed and needs updating.")
        exit(1)

    if os.path.isfile("/home/slave-nafsdm/config-legacy.conf"):
        logging.warning("Legacy config was found. This probably means that nafsdm has been upgraded but the config hasn't been changed yet.")
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
    checkUpdate(config)

    # run the daemon itself
    runDaemon(config)

if __name__ == "__main__":
    main()
    # graceful exit
    exit(0)
