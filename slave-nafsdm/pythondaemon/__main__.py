# nafsdm
# __main__
# get's stuff goooing

from daemonlog import *
from daemon import *
from version import version
from getConfig import getConfig
from versionCheck import checkUpdate

log("Welcome to Slave nafsdm version " + version)

if os.path.isfile("/home/slave-nafsdm/temp_upgrade.sh"):
    log("Upgrade script found. Please run the upgrade script before runing nafsdm-slave!")
    exit(1)

# check for new update
checkUpdate()

config = getConfig()

runDaemon(config)
