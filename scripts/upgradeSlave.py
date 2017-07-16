# nafsdm
# upgrade script for nafsdm slave
# Copyright Vilhelm Prytz 2017

# why have a seperate script for this? incase the thing needs more args than it knows

# imports
import subprocess

def initUpgrade(config):
    try:
        output = subprocess.check_output(["/bin/sh", "/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh", config.type])
    except Exception:
        # no point of logging anyways
        return "exception"

    return output
