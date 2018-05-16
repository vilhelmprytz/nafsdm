# nafsdm
# (c) Vilhelm Prytz 2018
# exitDaemon
# vital function for shutting down nafsdm-slave properly
# https://github.com/mrkakisen/nafsdm

# imports
import os

# shut down graceful
def gracefulExit(exitCode):
    os.remove("/home/slave-nafsdm/slave.pid")

    exit(int(exitCode))
