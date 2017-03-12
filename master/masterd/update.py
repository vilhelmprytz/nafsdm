# dns-manager
# update.py
# checks for updates and then updates the master from GitHub

def update(myVersion):
    logger.info("Checking for updates.")
    getVersion = urllib.urlopen("add url soon")
    if (getVersion == None or getVersion.getcode() != 200):
        logger.warning("No connection to GitHub.")
    else:
        if (myVersion == getVersion.read()):
            logger.info("You are running the latest version!")
        else:
            logger.info("Your version is " + myVersion + " but the latest version available is " + getVersion.read())
            # do the update thingy soon
