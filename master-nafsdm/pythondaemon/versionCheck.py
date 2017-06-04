# nafsdm
# versionCheck
# checks if a new version is available

from version import version
from daemonlog import log
import requests

def checkUpdate():
    log("Checking if a new version is available..")
    r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/masterVersion.txt")

    # check if we got a good code, requests has builtin codes which are OK
    if (r.status_code == requests.codes.ok):
        if (r.text.split("\n")[0] == version):
            log("You're running the latest version, " + version + "!")
        else:
            log("NOTICE: There is a new version available! New version: " + r.text.split("\n")[0])
    else:
        log("FATAL: Couldn't receive latest version (on GitHub). Quitting.")
        exit(1)
