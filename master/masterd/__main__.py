# dns-manager
# __main__.py
# first thing that starts, entry point (master)

# import
import logging
from version import __version__
from update import update

# check for updates and update
updateStatus = update() 
