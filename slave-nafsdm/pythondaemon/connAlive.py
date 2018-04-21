# nafsdm
# (c) Vilhelm Prytz 2018
# __main__
# connects to the master to say we're running
# https://github.com/mrkakisen/nafsdm

import logging
import subprocess
import time

def connectAlive(config):
    currentTime = time.strftime("%Y-%M-%d %H:%M:%S")

    try:
        output = subprocess.check_output(["ssh", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host, "/usr/bin/env", "echo", '"' + currentTime + '"', ">", "/home/master-nafsdm/slaveAlive/" + config.nodeName + ".slaveConn"])
    except Exception:
        logging.exception("An error occured during SSH connection.")
        logging.error("Could not update alive status - please check if the master is currently reachable.")

        return False

    # also set our connection interval
    try:
        output = subprocess.check_output(["ssh", "-i", "/home/slave-nafsdm/.ssh/master_key", config.user + "@" + config.host, "/usr/bin/env", "echo", '"' + config.update_interval + '"', ">", "/home/master-nafsdm/slaveAlive/" + config.nodeName + ".slaveInterval"])
    except Exception:
        logging.exception("An error occured during SSH connection.")
        logging.error("Could not update alive status - please check if the master is currently reachable.")

        return False

    return True
