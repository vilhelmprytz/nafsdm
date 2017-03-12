# dns-manager
# update.py
# checks for updates and then updates the master from GitHub

import logging
import urllib

def update(myVersion):
    logging.info("Checking for updates.")
    getVersion = urllib.urlopen("will be using own mirror instead")
    if (getVersion == None or getVersion.getcode() != 200):
        logging.warning("No connection to GitHub.")
    else:
        if (myVersion == getVersion.read()):
            logging.info("You are running the latest version!")
        else:
            logging.info("Your version is " + myVersion + " but the latest version available is " + getVersion.read())
            # do the update thingy soon
