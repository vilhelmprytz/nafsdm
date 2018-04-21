# nafsdm
# (c) Vilhelm Prytz 2017
# versionCheck
# checks if a new version is available
# https://github.com/mrkakisen/nafsdm

from version import version
import logging
import os
import requests
import os.path

github_branch = "master"
devIcMode = False
devStatus = False
doICUpdate = False
normalUpdate = False

# dev function for specifing branch
if os.path.isfile("/home/slave-nafsdm/pythondaemon/dev_github_branch.txt"):
    f = open("/home/slave-nafsdm/pythondaemon/dev_github_branch.txt")
    branchRaw = f.read()
    f.close()

    if "development" in branchRaw:
        github_branch = "development"

# dev mode, disables auto updater
if os.path.isfile("/home/slave-nafsdm/pythondaemon/dev_devmode.txt"):
    f = open("/home/slave-nafsdm/pythondaemon/dev_devmode.txt")
    devStatusRaw = f.read()
    f.close()
    if "True" in devStatusRaw:
        devStatus = True
    else:
        devStatus = False

# dev ic mode
if os.path.isfile("/home/master-nafsdm/pythondaemon/dev_ic_mode.txt"):
    f = open("/home/master-nafsdm/pythondaemon/dev_ic_mode.txt")
    devIcModeRaw = f.read()
    f.close()
    if "True" in devIcModeRaw:
        devIcMode = True
    else:
        devIcMode = False

def checkUpdate(config, mode):
    if devStatus == True:
        logging.warning("Developer mode enabled, skipping version checking.")
    else:
        if devIcMode:
            logging.info("Development commit update mode.")
            response = requests.get("https://api.github.com/repos/mrkakisen/nafsdm/branches/development")
            if (response.status_code == requests.codes.ok):
                data = response.json()
                latestCommit = data["commit"]["sha"][0:7]
                if version.split("-")[0] == latestCommit:
                    logging.info("You're using the latest development commit!")
                else:
                    doICUpdate = True
                    logging.info("A new update is available (dev commit - my version: " + version + " - latest version: " + latestCommit + "-dev)")
            else:
                logging.critical("Couldn't connect to GitHub! Quitting...")
                exit(1)
        else:
            logging.info("Checking if a new version is available..")
            r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/" + github_branch + "/version.txt")

            # check if we got a good code, requests has builtin codes which are OK
            if (r.status_code == requests.codes.ok):
                if (r.text.split("\n")[0] == version):
                    logging.info("You're running the latest version, " + version + "!")
                else:
                    normalUpdate = True

            if normalUpdate == True or doICUpdate == True:
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
                        if doICUpdate:

                        else:
                            upgradeStatus = initUpgrade(config, github_branch)
                        if upgradeStatus == "exception":
                            logging.critical("An error occured during upgrade. The script probably failed mid-through (that would break your installation). Please retry or run the script manually.")
                            exit(1)
                        elif upgradeStatus == "unsupported":
                            logging.warning("You're running an unsupported version - nafsdm will not be able to upgrade.")
                            logging.warning("Consider using developer mode to skip version checking.")
                            logging.info("nafsdm will continue boot")
                        elif upgradeStatus == "unknownException":
                            logging.critical("Unknown exception occured during upgrade.")
                            exit(1)
                        else:
                            f = open("/home/slave-nafsdm/upgradeLog.log", "w")
                            f.write(upgradeStatus)
                            f.close()
                            logging.info("Upgrade completed. Please update your configuration as the upgradeLog.log says.")
                            if mode == "cli":
                                logging.info("Upgrade command sent from CLI. Restarting nafsdm-slave..")
                                try:
                                    output = subprocess.check_output(["/bin/systemctl", "restart", "nafsdm-slave.service"])
                                except Exception:
                                    logging.exception("An error occured during systemd restart.")
                                    logging.error("Exit due to previous error.")
                                    exit(1)
                            else:
                                exit(0)
                    else:
                        logging.critical("Couldn't connect to GitHub! Quitting...")
                        exit(1)
                else:
                    logging.critical("Couldn't connect to GitHub! Quitting..")
                    exit(1)
        else:
            logging.critical("Couldn't receive latest version (on GitHub). Quitting.")
            exit(1)
