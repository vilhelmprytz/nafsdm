# dns-manager
# daemon.py
# handles daemon functions

# required header
import logging
import urllib
from log import setup_logging

# setup logging
logger = setup_logging()

# import
from flask import Flask

def start_daemon():
    logger.info("Starting daemon..")
    output = subprocess.call(["sh /etc/dns-manager/scripts/flask-start.sh"])
    logger.info("Daemon stoppped..")
