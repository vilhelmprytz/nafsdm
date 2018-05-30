# nafsdmctl
# connAlive
# connection alive status
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

import os
from os import listdir
from os.path import isfile, join
import subprocess
import time

# determine time ago
def timeAgo(filename):
    statbuf = os.stat(filename)
    modifiedTime = format(statbuf.st_mtime)
    epochAgo = int(float(time.time())) - int(float(modifiedTime))

    fullString = time.strftime('%M min(s) and %S sec(s) ago', time.localtime(epochAgo))

    if epochAgo > 3600:
        fullString = str(epochAgo/3600) + " hour(s) ago"

    if epochAgo > 86400:
        fullString = str(epochAgo/86400) + " day(s) ago"

    return fullString, epochAgo

def slaveConnections(colorStatus, bcolors):
    slaveConnections = []
    fileList = [f for f in listdir("/home/master-nafsdm/slaveAlive") if isfile(join("/home/master-nafsdm/slaveAlive", f))]

    for file in fileList:
        if ".slaveConn" in file:
            f = open("/home/master-nafsdm/slaveAlive/" + file, "r")
            slaveDate = f.read()
            f.close()

            f = open("/home/master-nafsdm/slaveAlive/" + file.split(".")[0] + ".slaveInterval")
            interval = f.read()
            f.close()

            timeAgoString, epochAgo = timeAgo("/home/master-nafsdm/slaveAlive/" + file)

            if int(epochAgo) > int(interval)+5:
                if colorStatus:
                    slaveConnections.append(["[" + bcolors.FAIL + "!" + bcolors.ENDC + "] " + file.split(".")[0], bcolors.FAIL + timeAgoString + bcolors.ENDC, slaveDate, interval])
                else:
                    slaveConnections.append(["[!] " + file.split(".")[0], timeAgoString, slaveDate, interval])
            else:
                if colorStatus:
                    slaveConnections.append([file.split(".")[0], bcolors.OKGREEN + timeAgoString + bcolors.ENDC, slaveDate, interval])
                else:
                    slaveConnections.append([file.split(".")[0], timeAgoString, slaveDate, interval])

    return slaveConnections

# deletes all slave connections
def flushSlaveConnections():
    fileList = [f for f in listdir("/home/master-nafsdm/slaveAlive") if isfile(join("/home/master-nafsdm/slaveAlive", f))]

    for file in fileList:
        try:
            os.remove("/home/master-nafsdm/slaveAlive/" + file)
        except Exception:
            print("failed to delete " + file)

    return True
