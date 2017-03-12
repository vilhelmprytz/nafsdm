# dns-manager
# __main__.py
# first thing that starts, entry point (master)

# import (required header)
import logging
from version import __version__
from update import update
from log import setup_logging
from daemon import start_daemon

# setup logging
logger = setup_logging()

# check for updates and update
updateStatus = update(__version__)

# start daemon in background
start_daemon()
