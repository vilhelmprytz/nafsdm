# nafsdm
# __main__
# get's stuff goooing

from daemonlog import *
from daemon import *
from version import __version__ as version
from getConfig import getConfig
from versionCheck import checkUpdate

log("Welcome to Slave nafsdm version " + version)

# check for new update
checkUpdate()

config = getConfig()

runDaemon(config)
