# nafsdm
# upgrade script for nafsdm master
# (c) Vilhelm Prytz 2017
# https://github.com/mrkakisen/nafsdm

# why have a seperate script for this? incase the thing needs more args than it knows

# imports
import subprocess

def initUpgrade(github_branch="master"):
    try:
        output = subprocess.check_output(["/bin/bash", "/home/master-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh", github_branch])
    except Exception:
        # no point of logging anyways
        return "exception"

    return output
