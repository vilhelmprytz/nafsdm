# dns-manager
# __main__
# masterd startup file

# imports
import os.path
from setup import setupSSH
from daemonlog import log
from __version__ import version

log("Master DNS manager starting up! Welcome! Running version " + version)

# check if first time
if not os.path.exists("/home/master-dnsman/.ssh"):
    log("SSH directory not found. Running first time setup!")
    setupSSH()

log("Master DNS daemon ready.")
