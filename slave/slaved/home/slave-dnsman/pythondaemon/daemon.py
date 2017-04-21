# dns-manager
# __main__
# daemon functions

from daemonlog import *
import time

def getData():


def writeData(data):

def reloadBind():


def runDaemon(config):
    log("Starting daemon.")

    endlessLoop = False
    while endlessLoop == False:
        time.sleep(int(config[2]))

        data = getData():
        writeData(data):
