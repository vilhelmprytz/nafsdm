# nafsdm-master daemon
# __main__
# daemon main file
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import logging
import os
import os.path
import psutil
from exitDaemon import *
from daemon import *
from getConfig import *
from versionCheck import *

# get version info
import sys
sys.path.insert(0, "/home/master-nafsdm/manager")

from version import version

# global vars
logPath = "/home/master-nafsdm/log.log"

# pre-checks
def preChecks(config):
    # before we do anything, we need to check there is no other instance of nafsdm-master daemon running
    if os.path.isfile("/home/master-nafsdm/daemon.pid"):
        try:
            f = open("/home/master-nafsdm/daemon.pid")
        except Exception, e:
            logging.exception("Could not read PID file (" + str(e) + ")")
            logging.critical("Exit due to previous error.")
            exit(1)

        pid = int(f.read())
        f.close()

        logging.info("Found PID " + str(pid) + " in file")

        # verify that there is an active process on that PID
        fail = True
        try:
            p = psutil.Process(pid)
        except Exception, e:
            # throws exception if pid does not
            logging.warning(str(e))
            logging.warning("Invalid PID found - nafsdm will boot anyways")

            # remove the file
            os.remove("/home/master-nafsdm/daemon.pid")

            # writePID function
            writePID()

            fail = False

        # we don't wan't to do this if it turns out the PID is not an active process
        if fail:
            # print error then exit
            logging.critical("Another process of nafsdm-master daemon is already running on PID " + str(pid))
            logging.critical("nafsdm-master daemon will not be able to start.")
            exit(1)
    else:
        logging.info("No other instances of nafsdm-master daemon found.")
        writePID()

    # crate zone folder if it doesn't exist
    if os.path.exists(config.master_zonePath):
        if not os.path.isdir(config.master_zonePath):
            # shouldn't happend
            logging.critical("Zone path exists but isn't a folder - please delete it before using nafsdm")
            gracefulExit(1)
    else:
        # if it doesn't exist, we will create it
        os.makedirs(config.master_zonePath)

    # check for new version
    checkUpdate(version)

# write our PID
def writePID():
    # get our PID using the psutil libs
    ourPID = os.getpid()

    try:
        f = open("/home/master-nafsdm/daemon.pid", "w")
        f.write(str(ourPID))
        f.close()
    except Exception, e:
        logging.exception("Could not write PID file.")
        logging.critical("Exit due to previous error.")
        gracefulExit(1)

    # log our PID
    logging.info("nafsdm-master daemon running on PID " + str(ourPID))

# main function
def main():
    # logger setup
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # format for logger
    formatter = logging.Formatter('DAEMON %(asctime)s %(levelname)s %(message)s')

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

    # welcome message
    logging.info("*******************************************************")
    logging.info("nafsdm-master daemon - running version " + version)
    logging.info("*******************************************************")

    # get the configuration file
    config = getConfig()

    # pre-start checks
    logging.info("Performing pre-start checks..")
    preChecks(config)
    logging.info("Pre-start checks passed!")

    # start daemon
    logging.info("Starting daemon..")
    runDaemon(config)
