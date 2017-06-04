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
        output = subprocess.check_output(["scp", "-i", "/home/slave-nafsdm/.ssh/master_key", config[1] + "@" + config[0] + ":/home/master-nafsdm/data/domains.txt", "/home/slave-nafsdm/domains.temp"])
    except Exception:
        if (sys.exc_info()[0] == "<class 'subprocess.CalledProcessError'>"):
            log("FATAL: Errors where encountered when trying to get domains data.")
            log("FATAL: Could not connect. Wrong password/key? Error message: " + str(sys.exc_info()[0]))
        else:
            log("FATAL: Errors where encountered when trying to get domains data.")
            log("FATAL: An unknown error occured. Error message: " + str(sys.exc_info()[0]))

def writeData(config):
    if os.path.isfile("/home/slave-nafsdm/domains.temp") == True:
        f = open("/home/slave-nafsdm/domains.temp")
        domainsData = f.read()
        f.close()

        # remove config temporarily
        if os.path.isfile(config[4]):
            os.remove(config[4])

        for currentLine in domainsData.split("\n"):
            if len(currentLine.split()) == 4:
                if config[5] in currentLine:
                    f = open(config[4], "a")
                    if config[3] == "debian" or config[3] == "ubuntu":
                        f.write("""/* """ + currentLine.split()[2] + """ */
zone '""" + currentLine.split()[0] + """' IN {
    type slave;
    file "db.""" + currentLine.split()[0] + """";
    masters { """ + currentLine.split()[1] + """; };
}; """ + "\n" + "\n")
                        f.close()
                    elif config[3] == "centos":
                        f.write("""/* """ + currentLine.split()[2] + """ */
zone '""" + currentLine.split()[0] + """' IN {
    type slave;
    file "slaves/""" + currentLine.split()[0] + """";
    masters { """ + currentLine.split()[1] + """; };
}; """ + "\n" + "\n")
                        f.close()
                    else:
                        log("FATAL: Invalid system type. Debian (ubuntu) & CentOS only supported.")
                        exit(1)
    else:
        log("FATAL: An error occured while reading data that was recently downloaded. This usually means the file never was downloaded and therefore doesn't exist.")
        log("FATAL: Couldn't read from domains file! Connection error?")

def reloadBind():
    f = open("/home/slave-nafsdm/domains.before")
    domainsBefore = f.read()
    f.close()

    f = open("/home/slave-nafsdm/domains.temp")
    domainsNew = f.read()
    f.close()

    if domainsBefore != domainsNew:
        log("Change detected! Reloading bind..")

        # if it fails, it will be printed in log
        log(subprocess.check_output(["rndc", "reconfig"]))

        # update the before file so reload doesn't occur again
        f = open("/home/slave-nafsdm/domains.before", "w")
        f.write(domainsNew)
        f.close()


def runDaemon(config):
    log("Daemon started!")

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config[2]))

        getData(config)
        writeData(config)
        reloadBind()
