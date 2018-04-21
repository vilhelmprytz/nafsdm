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
    epochAgo = int(float(time.time())) - int(float(modTime))

    return time.strftime('%M minute(s) and %S second(s) ago', time.localtime(epochAgo))

def slaveConnections(bcolors):
    slaveConnections = []
    fileList = [f for f in listdir("/home/master-nafsdm/slaveAlive") if isfile(join("/home/master-nafsdm/slaveAlive", f))]

    for file in fileList:
        if ".slaveConn" in file:
            f = open(file, "r")
            slaveDate = f.read()
            f.close()

            slaveConnections.append([file.split(".")[0], timeAgo(file), slaveDate])

    return slaveConnections
