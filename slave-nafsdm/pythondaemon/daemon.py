# nafsdm
# (c) Vilhelm Prytz 2017
# __main__
# daemon functions

import logging
import time
import os
import sys
import subprocess

def getData(config):
    try:
         outputNull = subprocess.check_output(["scp", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host + ":/home/master-nafsdm/data/domains.txt", "/home/slave-nafsdm/domains.temp"])
    except Exception:
        logging.exception("An error occured during SCP connection.")
        logging.error("Please check if the master is up and working.")

# find slave function
def find_slave(currentLine, myhostname):
    if not len(currentLine.split()) < 2:
        # split it by space
        split1 = currentLine.split()

        wasFound = False
        for currentSlave in split1[3].split("."):
            if currentSlave == myhostname:
                wasFound = True

        return wasFound

def writeData(config):
    if os.path.isfile("/home/slave-nafsdm/domains.temp") == True:
        f = open("/home/slave-nafsdm/domains.temp")
        domainsData = f.read()
        f.close()

        # remove config temporarily
        if os.path.isfile(config.bindPath):
            os.remove(config.bindPath)

        for currentLine in domainsData.split("\n"):
            if len(currentLine.split()) == 5:
                wasFound = find_slave(currentLine, config.nodeName)
                if (wasFound == True):
                    if len(currentLine.split()[4]) != 2:
                        if currentLine.split()[4].split(".")[1] == "yes":
                            f = open(config.bindPath, "a")
                            if config.type == "debian" or config.type == "ubuntu":
                                f.write('''/* ''' + currentLine.split()[2] + ''' */
zone "''' + currentLine.split()[0] + '''" IN {
    type slave;
    file "db.''' + currentLine.split()[0] + '''.signed";
    masters { ''' + currentLine.split()[1] + '''; };
}; ''' + "\n" + "\n")
                                f.close()
                            elif config.type == "centos":
                                f.write('''/* ''' + currentLine.split()[2] + ''' */
zone "''' + currentLine.split()[0] + '''" IN {
    type slave;
    file "slaves/''' + currentLine.split()[0] + '''.signed";
    masters { ''' + currentLine.split()[1] + '''; };
}; ''' + "\n" + "\n")
                                f.close()
                        elif currentLine.split()[4].split(".")[1] == "no":
                            f = open(config.bindPath, "a")
                            if config.type == "debian" or config.type == "ubuntu":
                                f.write('''/* ''' + currentLine.split()[2] + ''' */
zone "''' + currentLine.split()[0] + '''" IN {
    type slave;
    file "db.''' + currentLine.split()[0] + '''";
    masters { ''' + currentLine.split()[1] + '''; };
}; ''' + "\n" + "\n")
                                f.close()
                            elif config.type == "centos":
                                f.write('''/* ''' + currentLine.split()[2] + ''' */
zone "''' + currentLine.split()[0] + '''" IN {
    type slave;
    file "slaves/''' + currentLine.split()[0] + '''";
    masters { ''' + currentLine.split()[1] + '''; };
}; ''' + "\n" + "\n")
                                f.close()
                    else:
                        logging.critical("Invalid system type. Debian (ubuntu) & CentOS only supported.")
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
        logging.error("Due to the recent error, we will conrinue to try to reload bind.")
        reloadSucceeded = False

    if reloadSucceeded == True:
        # update the before file so reload doesn't occur again
        f = open("/home/slave-nafsdm/domains.before", "w")
        f.write(domainsNew)
        f.close()

def reloadBind():
    continueReload = True
    beforeExists = True
    if os.path.isfile("/home/slave-nafsdm/domains.before"):
        f = open("/home/slave-nafsdm/domains.before")
        domainsBefore = f.read()
        f.close()
    else:
        logging.warning("Couldn't read from before domains temp file. Is this the first time running maybe?")
        continueReload = True
        beforeExists = False

    if os.path.isfile("/home/slave-nafsdm/domains.temp"):
        f = open("/home/slave-nafsdm/domains.temp")
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
