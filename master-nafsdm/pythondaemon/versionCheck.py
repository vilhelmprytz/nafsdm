# nafsdm
# versionCheck
# checks if a new version is available

from version import version
from daemonlog import log
import os
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
            if (os.path.exists("/home/master-nafsdm/tempUpgrade")):
                log("WARN: folder already exists?")
            else:
                os.makedirs("/home/master-nafsdm/pythondaemon/tempUpgrade")
                # shortcut to make the shit importable
                f = open("/home/master-nafsdm/pythondaemon/tempUpgrade/__init__.py", "w")
                f.write(" ")
                f.close()

            # url must change from development to master before release!!
            url = ("https://raw.githubusercontent.com/MrKaKisen/nafsdm/development/scripts/upgradeMaster.sh")
            r = requests.get(url)
            if (r.status_code == requests.codes.ok):
                f = open("/home/master-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh")
                f.write(r.content)
                f.close()
                import subprocess
                outputNull = subprocess.check_output(["chmod", "+x", "/home/master-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh"])

                url = ("https://raw.githubusercontent.com/MrKaKisen/nafsdm/development/scripts/upgradeMaster.py")
                r = requests.get(url)
                if (r.status_code == requests.codes.ok):
                    f = open("/home/master-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.py")
                    f.write(r.content)
                    f.close()
                    import subprocess
                    outputNull = subprocess.check_output(["chmod", "+x", "/home/master-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.py"])

                    from tempUpgrade.temp_upgrade import initUpgrade
                    upgradeStatus = initUpgrade()
                    if upgradeStatus == "exception":
                        log("FATAL: An error occured during upgrade. Either you use a unsupported version or the script failed mid-through (that would break your installation). Please retry or run the script manually.")
                        exit(1)
                    else:
                        f = open("/home/master-master/upgradeLog.log")
                        f.write(upgradeStatus)
                        f.close()
                        log("INFO: Upgrade completed. Please update your configuration as the upgradeLog.log says.")
                else:
                    log("FATAL: Couldn't connect to GitHub! Quitting...")
                    exit(1)
            else:
                log("FATAL: Couldn't connect to GitHub! Quitting..")
                exit(1)
    else:
        log("FATAL: Couldn't receive latest version (on GitHub). Quitting.")
        exit(1)
