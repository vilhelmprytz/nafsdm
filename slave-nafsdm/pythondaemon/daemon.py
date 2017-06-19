# nafsdm
# __main__
# daemon functions

from daemonlog import *
import time
import os
import sys
import subprocess

def getData(config):
    try:
         outputNull = subprocess.check_output(["scp", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host + ":/home/master-nafsdm/data/domains.txt", "/home/slave-nafsdm/domains.temp"])
    except Exception:
        log("FATAL: An error occured during SCP connection. Running command again as output will be printed below: ")
        log(subprocess.check_output(["scp", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host + ":/home/master-nafsdm/data/domains.txt", "/home/slave-nafsdm/domains.temp"]))
        if (sys.exc_info()[0] == "<class 'subprocess.CalledProcessError'>"):
            log("FATAL: Errors where encountered when trying to get domains data.")
            log("FATAL: Could not connect. Wrong password/key? Error message: " + str(sys.exc_info()[0]))
        else:
            log("FATAL: Errors where encountered when trying to get domains data.")
            log("FATAL: An unknown error occured. Error message: " + str(sys.exc_info()[0]))

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
                        log("FATAL: Invalid system type. Debian (ubuntu) & CentOS only supported.")
                        exit(1)
    else:
        log("FATAL: An error occured while reading data that was recently downloaded. This usually means the file never was downloaded and therefore doesn't exist.")
        log("FATAL: Couldn't read from domains file! Connection error?")

def commandReload(domainsNew):
    # just to split things up

    # if it fails, it will be printed in log
    reloadSucceeded = True
    try:
        log(subprocess.check_output(["rndc", "reconfig"]))
    except Exception:
        log("FATAL: An error occured during bind reload. Run 'rndc reconfig' yourself to see why.")
        log("FATAL: Due to the error, we will conrinue to try to reload bind.")
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
        log("WARNING: Couldn't read from before domains temp file. Is this the first time running maybe?")
        continueReload = True
        beforeExists = False

    if os.path.isfile("/home/slave-nafsdm/domains.temp"):
        f = open("/home/slave-nafsdm/domains.temp")
        domainsNew = f.read()
        f.close()
    else:
        log("WARNING: Couldn't read from domains temp file. Is this the first time running maybe?")
        continueReload = False

    if (continueReload == True):
        if (beforeExists == True):
            if domainsBefore != domainsNew:
                log("Change detected! Reloading bind..")
                commandReload(domainsNew)
        else:
            log("No before file. Reloading bind..")
            commandReload(domainsNew)
    else:
        log("FATAL: Bind reload aborted due to earlier errors.")


def runDaemon(config):
    log("Daemon started!")

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
