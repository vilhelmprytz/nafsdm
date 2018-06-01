# nafsdmctl
# zone
# zone functions
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import subprocess
from db import *

# zone activate function - activates the zone management functionality and updates the db
def zoneActivate(domain):
    setIntValue(domain, "zoneManaged", "1")

# zone edit function - opens the editor for the
def zoneEdit(domain):
    print("coming soon..")
    exit(0)
