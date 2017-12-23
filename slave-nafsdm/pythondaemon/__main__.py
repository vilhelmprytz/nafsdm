# nafsdm
# (c) Vilhelm Prytz 2017
# __main__
# get's stuff goooing

from daemonlog import *
from daemon import *
from version import version
from getConfig import getConfig
from versionCheck import checkUpdate

log("Welcome to Slave nafsdm version " + version)

if os.path.isfile("/home/slave-nafsdm/tempUpgrade/temp_upgrade.sh"):
    log("Upgrade script found. Please delete the upgrade script before runing nafsdm-slave!")
    log("Note: the script is left there because the config has changed and needs updating.")
    exit(1)

if os.path.isfile("/home/slave-nafsdm/config-legacy.conf"):
    log("Legacy config was found. This probably means that nafsdm has upgraded but the config hasn't been changed yet.")
    exit(1)

# check for new update
config = getConfig()

checkUpdate(config)

runDaemon(config)
