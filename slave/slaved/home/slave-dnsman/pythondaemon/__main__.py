# dns-manager
# __main__
# get's stuff goooing

from daemonlog import *
from daemon import *
from version import __version__ as version
from getConfig import getConfig

log("Welcome to Slave DNS-manager version " + version)

config = getConfig()

runDaemon(config)
