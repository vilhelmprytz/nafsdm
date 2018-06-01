# nafsdm-master daemon
# exitDaemon
# exit daemon gracefully
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import os

# shut down graceful
def gracefulExit(exitCode):
    os.remove("/home/master-nafsdm/daemon.pid")

    exit(int(exitCode))
