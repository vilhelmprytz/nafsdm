# nafsdm
# versionCheck
# checks if a new version is available

from version import version
from daemonlog import log
import requests

def checkUpdate():
    log("Checking if a new version is available..")
    r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/version.txt")

    # check if we got a good code, requests has builtin codes which are OK
    if (r.status_code == requests.codes.ok):
        if (r.text.split("\n")[0] == version):
            log("You're running the latest version, " + version + "!")
        else:
            log("NOTICE: There is a new version available! New version: " + r.text.split("\n")[0])
            # url must change from development to master before release!!
            url = ("https://raw.githubusercontent.com/MrKaKisen/nafsdm/development/scripts/upgradeSlave.sh")
            r = requests.get(url)
            if (r.status_code == requests.codes.ok):
                f = open("/home/slave-nafsdm/temp_upgrade.sh")
                f.write(r.content)
                f.close()
                import subprocess
                outputNull = subprocess.check_output(["chmod", "+x", "/home/slave-nafsdm/temp_upgrade.sh"])

                log("NOTICE: Please run /home/slave-nafsdm/temp_upgrade.sh to upgrade!")
            else:
                log("FATAL: Couldn't connect to GitHub! Quitting..")
                exit(1)
    else:
        log("FATAL: Couldn't receive latest version (on GitHub). Quitting.")
        exit(1)
