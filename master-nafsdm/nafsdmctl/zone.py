# nafsdmctl
# zone
# zone functions
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import subprocess
from db import *
from getConfig import *

# zone activate function - activates the zone management functionality and updates the db
def zoneActivate(domain):
    setIntValue(domain, "zoneManaged", "1")

# zone edit function - opens the editor for the
def zoneEdit(id):
    # retrieve the configuration class
    config = getConfig()

    try:
        output = subprocess.call(["/usr/bin/editor", config.master_zonePath + "/id" + str(id) + ".zone"])
    except Exception:
        return False

    return True

# reload bind function
def zoneReload():
    # we will just send a simple rndc reload command
    try:
        output = subprocess.check_output(["rndc", "reload"])
    except Exception:
        return False

    return True
