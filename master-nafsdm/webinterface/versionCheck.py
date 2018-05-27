# nafsdm webinterface
# versionCheck
# checks if a new version is available
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

import os
import requests
import os.path
import logging

# import master version
import sys
sys.path.insert(0, "/home/master-nafsdm/pythondaemon")
from version import version as masterVersion

github_branch = "master"
devIcMode = False
doICUpdate = False
normalUpdate = False

# dev function for specifing branch
if os.path.isfile("/home/master-nafsdm/pythondaemon/dev_github_branch.txt"):
    f = open("/home/master-nafsdm/pythondaemon/dev_github_branch.txt")
    branchRaw = f.read()
    f.close()

    if "development" in branchRaw:
        github_branch = "development"

# dev ic mode
if os.path.isfile("/home/master-nafsdm/pythondaemon/dev_ic_mode.txt"):
    f = open("/home/master-nafsdm/pythondaemon/dev_ic_mode.txt")
    devIcModeRaw = f.read()
    f.close()
    if "True" in devIcModeRaw:
        devIcMode = True
    else:
        devIcMode = False

def checkUpdate():
    normalUpdate = False
    doICUpdate = False
    if devIcMode:
        loggin.info("Development commit update mode.")
        response = requests.get("https://api.github.com/repos/mrkakisen/nafsdm/branches/development")
        if (response.status_code == requests.codes.ok):
            data = response.json()
            latestCommit = data["commit"]["sha"][0:7]
            if version.split("-")[0] == latestCommit:
                logging.info("You're using the latest development commit!")
                return True, devIcMode, github_branch, version, latestCommit
            else:
                logging.info("A new update is available (dev commit - my version: " + version + " - latest version: " + latestCommit + "-dev)")
                return True, devIcMode, github_branch, version, latestCommit
        else:
            logging.critical("Couldn't connect to GitHub! Quitting...")
            return False, devIcMode, github_branch, version, None

    else:
        logging.info("Checking if a new version is available..")
        r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/" + github_branch + "/version.txt")

        # check if we got a good code, requests has builtin codes which are OK
        if (r.status_code == requests.codes.ok):
            if (r.text.split("\n")[0] == version):
                logging.info("You're running the latest version, " + version + "!")
                normalUpdate = False
                return True, devIcMode, github_branch, version, r.text.split("\n")[0]
            else:
                logging.info("There is a new version available! New version: " + r.text.split("\n")[0])
                return True, devIcMode, github_branch, version, r.text.split("\n")[0]
        else:
            logging.critical("Couldn't connect to GitHub! Quitting...")
            return False, devIcMode, github_branch, version, None
