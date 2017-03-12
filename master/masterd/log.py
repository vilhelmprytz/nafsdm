# dns-manager
# log.py
# sets up log stuf

import logging
import sys

def setup_logging():
    # critical events will log in console, non in file
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("/etc/dns-manager/logs/master.log")
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # do not set the format for the console handler

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
