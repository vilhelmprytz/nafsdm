# dns-manager
# log.py
# sets up log stuf

import logging
import sys

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logco = logging.StreamHandler(sys.stdout)
    logco.setLevel(logging.DEBUG)
    
    logger.addHandler(logco)
    #logging.basicConfig(filename="/etc/dns-manager/logs/master.log",level=logging.DEBUG)
