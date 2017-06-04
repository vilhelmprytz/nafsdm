# nafsdm
# __main__
# masterd startup file

# imports
import os.path
from setup import setupSSH
from daemonlog import log
from __version__ import version
from versionCheck import checkUpdate

log("Master nafsdm starting up! Welcome! Running version " + version)

# check if first time
if not os.path.isfile("/home/master-nafsdm/.ssh/nafsdm_rsa"):
    log("SSH directory not found. Running first time setup!")
    setupSSH()

# check for new update
checkUpdate()

log("Master DNS daemon ready.")
