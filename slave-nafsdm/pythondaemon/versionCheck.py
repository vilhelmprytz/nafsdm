# nafsdm
# (c) Vilhelm Prytz 2017
# versionCheck
# checks if a new version is available

from version import version
import logging
import os
import requests
import os.path

github_branch = "master"

# dev function for specifing branch
if os.path.isfile("/home/slave-nafsdm/pythondaemon/dev_github_branch.txt"):
    f = open("/home/slave-nafsdm/pythondaemon/dev_github_branch.txt")
    branchRaw = f.read()
    f.close()

    if "development" in branchRaw:
        github_branch = "development"

def checkUpdate(config):
    logging.info("Checking if a new version is available..")
    r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/" + github_branch + "/version.txt")

    # check if we got a good code, requests has builtin codes which are OK
    if (r.status_code == requests.codes.ok):
        if (r.text.split("\n")[0] == version):
            logging.info("You're running the latest version, " + version + "!")
        else:
            logging.info("There is a new version available! New version: " + r.text.split("\n")[0])
            if (os.path.exists("/home/slave-nafsdm/tempUpgrade")):
                logging.warning("Temp upgrade folder already exists?")
            else:
                os.makedirs("/home/slave-nafsdm/pythondaemon/tempUpgrade")
                # shortcut to make the shit importable
                f = open("/home/slave-nafsdm/pythondaemon/tempUpgrade/__init__.py", "w")
                f.write(" ")
                f.close()

            # url must change from development to master before release!!
            url = ("https://raw.githubusercontent.com/MrKaKisen/nafsdm/" + github_branch + "/scripts/upgradeSlave.sh")
            r = requests.get(url)
            if (r.status_code == requests.codes.ok):
                f = open("/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh", "w")
                f.write(r.content)
                f.close()
                import subprocess
                outputNull = subprocess.check_output(["chmod", "+x", "/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh"])

                url = ("https://raw.githubusercontent.com/MrKaKisen/nafsdm/" + github_branch + "/scripts/upgradeSlave.py")
                r = requests.get(url)
                if (r.status_code == requests.codes.ok):
                    f = open("/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.py", "w")
                    f.write(r.content)
                    f.close()
                    import subprocess
                    outputNull = subprocess.check_output(["chmod", "+x", "/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.py"])

                    from tempUpgrade.temp_upgrade import initUpgrade
                    upgradeStatus = initUpgrade(config)
                    if upgradeStatus == "exception":
                        logging.critical("An error occured during upgrade. Either you use a unsupported version or the script failed mid-through (that would break your installation). Please retry or run the script manually.")
                        exit(1)
                    else:
                        f = open("/home/slave-nafsdm/upgradeLog.log", "w")
                        f.write(upgradeStatus)
                        f.close()
                        logging.info("Upgrade completed. Please update your configuration as the upgradeLog.log says.")
                        logging.info("nafsdm will continue to boot but into the old version (libs already loaded :P)")
                else:
                    logging.critical("Couldn't connect to GitHub! Quitting...")
                    exit(1)
            else:
                logging.critical("Couldn't connect to GitHub! Quitting..")
                exit(1)
    else:
        logging.critical("Couldn't receive latest version (on GitHub). Quitting.")
        exit(1)
