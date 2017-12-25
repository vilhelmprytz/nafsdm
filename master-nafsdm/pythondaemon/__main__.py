# nafsdm
# __main__
# masterd startup file

# imports
import os.path
from setup import setupSSH
from daemonlog import log
from version import version
from versionCheck import checkUpdate

log("Master nafsdm starting up! Welcome! Running version " + version)

# pre checks
if not os.path.isfile("/home/master-nafsdm/.ssh/nafsdm_rsa"):
    log("SSH directory not found. Running first time setup!")
    setupSSH()

# check for upgrade script
if os.path.isfile("/home/master-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh"):
    log("Upgrade script found. Please change the data file and remove upgrade script!")
    exit(1)

# check for the legacy domains.txt file (before version 1.2.3)
if os.path.isfile("/home/master-nafsdm/data/domains.txt"):
    log("Legacy domains.txt file found. Please delete it before using nafsdm.")
    exit(1)

# check if the new (after version 1.2.3) domains.sql file is present
if not os.path.isfile("/home/master-nafsdm/data/domains.sql"):
    log("Could not find the domains.sql file. Configuring database..")
    setupDatabase()

# check for new update
checkUpdate()

log("Master DNS daemon ready.")
