# nafsdm
# upgrade script for nafsdm slave
# (c) Vilhelm Prytz 2017
# https://github.com/mrkakisen/nafsdm

# why have a seperate script for this? incase the thing needs more args than it knows

# imports
import subprocess

def initUpgrade(config):
    try:
        output = subprocess.check_output(["/bin/bash", "/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh", config.type])
    except Exception:
        # no point of logging anyways
        return "exception"

    return output
