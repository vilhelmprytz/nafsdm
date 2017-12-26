# nafsdm
# (c) Vilhelm Prytz 2017
# __main__
# daemon functions

import logging
import time
import os
import sys
import subprocess
import db
from shutil import copyfile

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
                os.remove(config.bindPath)

            for r in domainsToWrite:
                if r[5] == "y":
                    f = open(config.bindPath, "a")
                    if config.type == "debian" or config.type == "ubuntu":
                        f.write('''/* ''' + currentLine.split()[2] + ''' */
zone "''' + r[1] + '''" IN {
    type slave;
    file "db.''' + r[1] + '''.signed";
    masters { ''' + r[2] + '''; };
}; ''' + "\n" + "\n")
                        f.close()
                    elif config.type == "centos":
                        f.write('''/* ''' + currentLine.split()[2] + ''' */
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
                        f.write('''/* ''' + currentLine.split()[2] + ''' */
zone "''' + r[1] + '''" IN {
    type slave;
    file "db.''' + r[1] + '''";
    masters { ''' + r[2] + '''; };
}; ''' + "\n" + "\n")
                        f.close()
                    elif config.type == "centos":
                        f.write('''/* ''' + currentLine.split()[2] + ''' */
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
    else:
        logging.error("An error occured while reading data that was recently downloaded. This usually means the file never was downloaded and therefore doesn't exist.")
        logging.error("Couldn't read from domains file! Connection error?")

def commandReload(domainsNew):
    # just to split things up

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

def reloadBind():
    continueReload = True
    beforeExists = True
    if os.path.isfile("/home/slave-nafsdm/temp/domains_before.sql"):
        f = open("/home/slave-nafsdm/temp/domains_before.sql")
        domainsBefore = f.read()
        f.close()
    else:
        logging.warning("Couldn't read from before domains temp file. Is this the first time running maybe?")
        continueReload = True
        beforeExists = False

    if os.path.isfile("/home/slave-nafsdm/temp/domains_temp.sql"):
        f = open("/home/slave-nafsdm/temp/domains_temp.sql")
        domainsNew = f.read()
        f.close()
    else:
        logging.warning("Couldn't read from domains temp file. Is this the first time running maybe?")
        continueReload = False

    if (continueReload == True):
        if (beforeExists == True):
            if domainsBefore != domainsNew:
                logging.info("Change detected! Reloading bind..")
                commandReload(domainsNew)
        else:
            logging.info("No before file. Reloading bind..")
            commandReload(domainsNew)
    else:
        logging.error("Bind reload aborted due to earlier errors.")


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
        writeData(config)
        reloadBind()
