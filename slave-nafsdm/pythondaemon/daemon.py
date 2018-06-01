# nafsdm
# (c) Vilhelm Prytz 2018
# __main__
# daemon functions
# https://github.com/mrkakisen/nafsdm

import logging
import time
import os
import sys
import subprocess
import signal
from exitDaemon import *
from db import parseDbData
from shutil import copyfile
from version import version
from connAlive import connectAlive

# catch SIGTERM
def sigterm_handler(signal, frame):
    # exit gracefully
    gracefulExit(0)

# catches it
signal.signal(signal.SIGTERM, sigterm_handler)

def changeDetected():
    changeDetected = None
    beforeExists = None
    tempExists = None

    if os.path.isfile("/home/slave-nafsdm/temp/domains_before.sql"):
        f = open("/home/slave-nafsdm/temp/domains_before.sql")
        domainsBefore = f.read()
        f.close()
        beforeExists = True
    else:
        logging.warning("Couldn't read from before domains temp file. Is this the first time running maybe?")
        beforeExists = False

    if os.path.isfile("/home/slave-nafsdm/temp/domains_temp.sql"):
        f = open("/home/slave-nafsdm/temp/domains_temp.sql")
        domainsNew = f.read()
        f.close()
        tempExists = True
    else:
        logging.warning("Couldn't read from domains temp file. Is this the first time running maybe?")
        tempExists = False

    if tempExists == True and beforeExists == True:
        if domainsBefore != domainsNew:
            changeDetected = True
        else:
            changeDetected = False
    else:
        changeDetected = False

    return changeDetected

# gets the version of the master and checks if it matches up with ours
def checkMasterVersion(config):
    logging.info("Fetching master's version..")
    try:
        output = subprocess.check_output(["ssh", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host, "/usr/bin/env", "cat", "/home/master-nafsdm/manager/version.py"])
    except Exception:
        logging.exception("An error occured during SSH connection.")
        logging.error("Please check if the master is currently reachable.")

        return False

    try:
        masterVersion = output.split("\n")[0].split()[2].split('"')[1]
    except Exception:
        logging.exception("Invalid version response from master.")
        logging.error("Response from master: " + str(output))

        return False

    if version == masterVersion:
        logging.info("We're running the same version as the master!")

        return True
    else:
        logging.critical("We're NOT running the same version as the master! (my version: " + str(version) + " - Master version: " + masterVersion + ")")
        logging.critical("nafsdm-slave daemon will not be able to start.")
        gracefulExit(1)


# get CLI state
def CLIStateCheck():
    try:
        f = open("/home/slave-nafsdm/pythondaemon/cli_state")
    except Exception:
        return False, None

    stateRaw = f.read()
    f.close()

    # remove the file
    os.remove("/home/slave-nafsdm/pythondaemon/cli_state")

    return True, stateRaw

def getData(config):
    try:
         outputNull = subprocess.check_output(["scp", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host + ":/home/master-nafsdm/data/domains.sql", "/home/slave-nafsdm/temp/domains_temp.sql"])
    except Exception:
        logging.exception("An error occured during SCP connection.")
        logging.error("Please check if the master is up and reachable.")

def writeData(config):
    if os.path.isfile("/home/slave-nafsdm/temp/domains_temp.sql") == True:
        domainsToWrite = parseDbData(config)
        if domainsToWrite != False:

            # remove config temporarily
            if os.path.isfile(config.bindPath):
                logging.debug("Removing config temporarily")
                os.remove(config.bindPath)

            # test if there is a folder available
            try:
                ftest = open(config.bindPath, "w")
            except Exception:
                logging.exception("Couldn't write to bind file.")
                logging.error("Please check if the folder exists.")

                return False

            invalidSystemType = False
            for r in domainsToWrite:
                if r[5] == "y":
                    f = open(config.bindPath, "a")
                    if config.type == "debian" or config.type == "ubuntu":
                        f.write('''/* ''' + r[3] + ''' */
zone "''' + r[1] + '''" IN {
    type slave;
    file "db.''' + r[1] + '''.signed";
    masters { ''' + r[2] + '''; };
}; ''' + "\n" + "\n")
                        f.close()
                    elif config.type == "centos":
                        f.write('''/* ''' + r[3] + ''' */
zone "''' + r[1] + '''" IN {
    type slave;
    file "slaves/''' + r[1] + '''.signed";
    masters { ''' + r[2] + '''; };
}; ''' + "\n" + "\n")
                        f.close()
                    else:
                        invalidSystemType = True
                elif r[5] == "n":
                    f = open(config.bindPath, "a")
                    if config.type == "debian" or config.type == "ubuntu":
                        f.write('''/* ''' + r[3] + ''' */
zone "''' + r[1] + '''" IN {
    type slave;
    file "db.''' + r[1] + '''";
    masters { ''' + r[2] + '''; };
}; ''' + "\n" + "\n")
                        f.close()
                    elif config.type == "centos":
                        f.write('''/* ''' + r[3] + ''' */
zone "''' + r[1] + '''" IN {
    type slave;
    file "slaves/''' + r[1] + '''";
    masters { ''' + r[2] + '''; };
}; ''' + "\n" + "\n")
                        f.close()
                    else:
                        invalidSystemType = True
            if invalidSystemType == True:
                logging.critical("Invalid system type! Please check your config!")
                gracefulExit(1)
            logging.debug("New config has been written.")
    else:
        logging.error("An error occured while reading data that was recently downloaded. This usually means the file never was downloaded and therefore doesn't exist.")

def reloadBind():
    # if it fails, it will be printed in log
    reloadSucceeded = True
    logging.info("Reloading bind..")
    try:
        logging.info("Reload output (should be empty if ok): " + subprocess.check_output(["rndc", "reconfig"]))
    except Exception:
        logging.exception("An error occured during bind reload.")
        logging.error("Due to previous error, nafsdm will retry bind reload.")
        reloadSucceeded = False

    if reloadSucceeded == True:
        # update the before file so reload doesn't occur again
        try:
            copyfile("/home/slave-nafsdm/temp/domains_temp.sql", "/home/slave-nafsdm/temp/domains_before.sql")
        except Exception:
            logging.exception("Error occured during file replacement (domains_temp to domains_before).")
            logging.error("Do we have permissions to that folder?")


def runDaemon(config):
    logging.info("Starting daemon..")

    # run everything once as we get immediate output if everything is OK
    versionCheck = checkMasterVersion(config)
    if versionCheck == False:
        logging.warning("Skipping master version check step..")
    # connect alive
    if connectAlive(config) == False:
        logging.warning("Could not write alive status.")
    getData(config)
    writeData(config)
    reloadBind()

    logging.info("Daemon started!")

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config.update_interval))

        # check for new CLI state
        CLIstatus, stateRaw = CLIStateCheck()
        if CLIstatus:
            if stateRaw == "upgrade":
                logging.info("Upgrade command received from CLI!")
                from versionCheck import checkUpdate
                checkUpdate(config, "cli")

        getData(config)
        changeStatus = changeDetected()
        if changeStatus == True:
            logging.info("Change detected! Writing configuration & reloading bind")
            writeData(config)
            reloadBind()

        # connect alive
        if connectAlive(config) == False:
            logging.warning("Could not write alive status.")
