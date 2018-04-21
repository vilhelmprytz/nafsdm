# nafsdm
# upgrade script for nafsdm slave
# (c) Vilhelm Prytz 2017
# https://github.com/mrkakisen/nafsdm

# why have a seperate script for this? incase the thing needs more args than it knows

# imports
import subprocess

# import version
import sys
sys.path.insert(0, "/home/slave-nafsdm/pythondaemon")
from version import version

def initUpgrade(config, github_branch="master", dev_ic_mode=False):
    try:
        output = subprocess.check_output(["/bin/bash", "/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh", config.type, github_branch, dev_ic_mode])
    except subprocess.CalledProcessError as grepexc:
        # we want grepexc to determine the exit code (if it's an issue or just unsupported version)
        exit_code = grepexc.returncode

        # these versions cannot tell the difference between unsupported and exception and has therefore their own section in this script
        if version == "1.2.5-stable" or version == "1.2.4-stable" or version == "1.2.3-stable" or version == "1.2.2-stable" or version == "1.2.1-stable" or version == "1.2-stable" or version == "1.1-stable" or version == "1.0.1-stable":
            return "exception"
        else:
            # return different depending on exit code (for versions after 1.2.5-stable)
            if int(exit_code) == 128:
                return "unsupported"
            if int(exit_code) == 1:
                return "exception"
            else:
                return "unknownException"

    return output
