# dns-manager
# update.py
# checks for updates and then updates the master from GitHub

# required header
import logging
import urllib
from log import setup_logging

# setup logging
logger = setup_logging()

def update(myVersion):
    logger.debug("Checking for updates.")
    getVersion = urllib.urlopen("https://mirror.mrkakisen.net/dns-manager/master-version.latest")
    if (getVersion == None or getVersion.getcode() != 200):
        logger.warning("No connection to GitHub.")
    else:
        if (myVersion == getVersion.read()):
            logger.debug("You are running the latest version!")
        else:
            logger.debug("Your version is " + myVersion + " but the latest version available is " + getVersion.read())
            # do the update thingy soon
