# dns-manager
# __main__
# daemon functions

from daemonlog import *
import time

def getData(config):
    try:
        subprocess.check_output(['ssh', config[1] + '@' + config[0], '"cat',  '>', '/home/master-masterdnsman/data/domains.txt"', '|', '>', '/home/slave-dnsman/domains.temp'])
    except Exception:
        if sys.exc_info()[0] == "<class 'subprocess.CalledProcessError'>"):
            log("FATAL: Could not connect. Wrong password? Error message: " + sys.exc_info()[0])
        else:
            log("FATAL: An unknown error occured. Error message: " + sys.exc_info()[0])

def writeData(data):
    f = open("/home/slave-dnsman/domains.temp")
    domains = f.read()
    f.close()

    try:
        f = open("BINDPATH")
        f.write(domains)
        f.close()
    except Exception:
        log("FATAL: Can not write to bind. err: " + sys.exc_info()[0])
def reloadBind():


def runDaemon(config):
    log("Starting daemon.")

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config[3]))

        getData(config):
        writeData():
