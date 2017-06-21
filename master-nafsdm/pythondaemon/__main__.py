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

# check if first time
if not os.path.isfile("/home/master-nafsdm/.ssh/nafsdm_rsa"):
    log("SSH directory not found. Running first time setup!")
    setupSSH()

if os.path.isfile("/home/slave-nafsdm/temp_upgrade.sh"):
    log("Upgrade script found. Please run the upgrade script before runing nafsdm-slave!")
    exit(1)

# check for new update
checkUpdate()

log("Master DNS daemon ready.")
