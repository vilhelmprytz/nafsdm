# nafsdm-master daemon
# versionCheck
# daemon version check file
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

import logging
import os
import requests
import os.path
from exitDaemon import *

github_branch = "master"
devIcMode = False
devStatus = False
doICUpdate = False
normalUpdate = False

# dev function for specifing branch
if os.path.isfile("/home/master-nafsdm/manager/dev_github_branch.txt"):
    f = open("/home/master-nafsdm/manager/dev_github_branch.txt")
    branchRaw = f.read()
    f.close()

    if "development" in branchRaw:
        github_branch = "development"

# dev mode, disables auto updater
if os.path.isfile("/home/master-nafsdm/manager/dev_devmode.txt"):
    f = open("/home/master-nafsdm/manager/dev_devmode.txt")
    devStatusRaw = f.read()
    f.close()
    if "True" in devStatusRaw:
        devStatus = True
    else:
        devStatus = False

# dev ic mode
if os.path.isfile("/home/master-nafsdm/manager/dev_ic_mode.txt"):
    f = open("/home/master-nafsdm/manager/dev_ic_mode.txt")
    devIcModeRaw = f.read()
    f.close()
    if "True" in devIcModeRaw:
        devIcMode = True
    else:
        devIcMode = False

def checkUpdate(version):
    normalUpdate = False
    doICUpdate = False
    if devStatus == True:
        logging.info("Developer mode enabled, skipping version checking.")
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
                    logging.warning("A new update is available (dev commit - my version: " + version + " - latest version: " + latestCommit + "-dev)")
            else:
                logging.critical("Failed to establish connection to GitHub! Exit due to error.")
                gracefulExit(1)
        else:
            logging.info("Checking if a new version is available..")
            r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/" + github_branch + "/version.txt")

            # check if we got a good code, requests has builtin codes which are OK
            if (r.status_code == requests.codes.ok):
                if (r.text.split("\n")[0] == version):
                    logging.info("You're running the latest version, " + version + "!")
                    normalUpdate = False
                else:
                    logging.warning("There is a new version available! New version: " + r.text.split("\n")[0])
                    normalUpdate = True

        if normalUpdate == True or doICUpdate == True:
            logging.info("To update nafsdm, please run 'nafsdm-manager' in the console to trigger the update.")
