# nafsdm
# (c) Vilhelm Prytz 2017
# __main__
# daemon functions

import logging
import time
import os
import sys
import subprocess
from db import parseDbData
from shutil import copyfile

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

def getData(config):
    try:
         outputNull = subprocess.check_output(["scp", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host + ":/home/master-nafsdm/data/domains.sql", "/home/slave-nafsdm/temp/domains_temp.sql"])
    except Exception:
        logging.exception("An error occured during SCP connection.")
        logging.error("Please check if the master is up and working.")

def writeData(config):
    if os.path.isfile("/home/slave-nafsdm/temp/domains_temp.sql") == True:
        domainsToWrite = parseDbData(config)
        if domainsToWrite != False:

            # remove config temporarily
            if os.path.isfile(config.bindPath):
                logging.debug("Removing config temporarily")
                os.remove(config.bindPath)

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
                exit(1)
            logging.debug("New config has been written.")
    else:
        logging.error("An error occured while reading data that was recently downloaded. This usually means the file never was downloaded and therefore doesn't exist.")
        logging.error("Couldn't read from domains file! Connection error?")

def reloadBind():
    # if it fails, it will be printed in log
    reloadSucceeded = True
    try:
        logging.info("Reload output (should be empty if ok): " + subprocess.check_output(["rndc", "reconfig"]))
    except Exception:
        logging.exception("An error occured during bind reload.")
        logging.error("Due to the recent error, we will continue to try to reload bind.")
        reloadSucceeded = False

    if reloadSucceeded == True:
        # update the before file so reload doesn't occur again
        try:
            copyfile("/home/slave-nafsdm/temp/domains_temp.sql", "/home/slave-nafsdm/temp/domains_before.sql")
        except Exception:
            logging.exception("Error occured during file replacement domains_temp to domains_before.")
            logging.error("Do we have permissions to that folder?")


def runDaemon(config):
    logging.info("Daemon started!")

    # run everything once as we get immediate output if everything is OK
    getData(config)
    writeData(config)
    reloadBind()

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config.update_interval))

        getData(config)
        changeStatus = changeDetected()
        if changeStatus == True:
            logging.info("Change detected! Writing configuration & reloading bind")
            writeData(config)
            reloadBind()
