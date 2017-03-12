# dns-manager
# log.py
# sets up log stuf

import logging

def setup_logging():
    logging.basicConfig(filename="/etc/dns-manager/logs/master.log",level=logging.DEBUG)
