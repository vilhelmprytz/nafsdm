# nafsdm
# __main__
# daemon functions

from daemonlog import *
import time
import os
import sys

def getData(config):
    try:
        subprocess.check_output(['ssh', '-i', "/home/slave-nafsdm/.ssh/master_key", config[1] + '@' + config[0], '"cat',  '>', '/home/master-nafsdm/data/domains.txt"', '|', '>', '/home/slave-nafsdm/domains.temp'])
    except Exception:
        if (sys.exc_info()[0] == "<class 'subprocess.CalledProcessError'>"):
            log("FATAL: Could not connect. Wrong password/key? Error message: " + str(sys.exc_info()[0]))
        else:
            log("FATAL: An unknown error occured. Error message: " + str(sys.exc_info()[0]))

def writeData():
    f = open("/home/slave-nafsdm/domains.temp")
    domainsData = f.read()
    f.close()

    # remove config temporarily
    os.remove(config[4])

    for currentLine in domainsData.split("\n"):
        if len(currentLine.split()) != 4:
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

def reloadBind():
    print("coming soon")

def runDaemon(config):
    log("Starting daemon.")

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config[2]))

        getData(config)
        writeData()
