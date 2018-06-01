# nafsdm
# upgrade script for nafsdm master
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# why have a seperate script for this? incase the thing needs more args than it knows

# imports
import subprocess
import os.path
import sys

# import version (has changed in 1.4, we need to check which folder the uses has their version in)
if os.path.isfile("/home/master-nafsdm/pythondaemon"):
    sys.path.insert(0, "/home/master-nafsdm/pythondaemon")
    from version import version
else:
    sys.path.insert(0, "/home/master-nafsdm/manager")
    from version import version

def initUpgrade(github_branch="master", dev_ic_mode=False):
    try:
        output = subprocess.check_output(["/bin/bash", "/home/master-nafsdm/manager/tempUpgrade/temp_upgrade.sh", github_branch, str(dev_ic_mode)])
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
