# dns-manager
# __main__
# daemon functions

from daemonlog import *
import time
import os

def getData(config):
    try:
        subprocess.check_output(['ssh', config[1] + '@' + config[0], '"cat',  '>', '/home/master-masterdnsman/data/domains.txt"', '|', '>', '/home/slave-dnsman/domains.temp'])
    except Exception:
        if sys.exc_info()[0] == "<class 'subprocess.CalledProcessError'>"):
            log("FATAL: Could not connect. Wrong password/key? Error message: " + sys.exc_info()[0])
        else:
            log("FATAL: An unknown error occured. Error message: " + sys.exc_info()[0])

def writeData():
    f = open("/home/slave-dnsman/domains.temp")
    domainsData = f.read()
    f.close()

    # remove config temporarily
    os.remove(config[4])

    for currentLine in domainsData.split("\n"):
        if not len(currentLine) < 2:
            f = open(config[4], "a")
            if config[3] == "debian":
                f.write("""/* """ + currentLine.split("")[2] + """ */
zone """"" + currentLine.split("")[0] + """"" IN {
    type slave;
    file "db.""" + currentLine.split("")[0] + """";
    masters { """ + currentLine.split("")[0] + """; };
}; """)
                f.close()
            elif config[3] == "centos":
                # adding soon
            else:
                log("FATAL: Invalid system type. Debian & CentOS only supported (if ubuntu, type debian)")
                exit(0)

def reloadBind():


def runDaemon(config):
    log("Starting daemon.")

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config[2]))

        getData(config):
        writeData():
