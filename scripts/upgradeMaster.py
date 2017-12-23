# nafsdm
# upgrade script for nafsdm master
# (c) Vilhelm Prytz 2017

# why have a seperate script for this? incase the thing needs more args than it knows

# imports
import subprocess

def initUpgrade():
    try:
        output = subprocess.check_output(["/bin/bash", "/home/master-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh"])
    except Exception:
        # no point of logging anyways
        return "exception"

    return output
