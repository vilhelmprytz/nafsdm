# dns-manager
# __main__
# daemon functions

from daemonlog import *
import time

def getData(config):
    try:
        subprocess.check_output(["ssh", "" + config[1] "@" + config[0]])
    except Exception:
        if sys.exc_info()[0] == "<class 'subprocess.CalledProcessError'>"):
            log("FATAL: Could not connect. Wrong password? Error message: " + sys.exc_info()[0])
        else:
            log("FATAL: An unknown error occured. Error message: " + sys.exc_info()[0])

def writeData(data):

def reloadBind():


def runDaemon(config):
    log("Starting daemon.")

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config[3]))

        data = getData(config):
        writeData(data):
