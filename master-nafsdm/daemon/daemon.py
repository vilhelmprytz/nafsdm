# nafsdm-master daemon
# daemon
# daemon file
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import logging
import time
import os.path
import signal
from exitDaemon import *
from db import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# catch SIGTERM
def sigterm_handler(signal, frame):
    # exit gracefully
    gracefulExit(0)

# catches it
signal.signal(signal.SIGTERM, sigterm_handler)

# functions
def updateConfiguration(config):
    # get all domains from configuration
    domainsRaw = listDomains()

    domainsAdded = 0
    for row in domainsRaw:
        if row != None:
            if str(row[6]) == "1":
                domainsAdded = createEmptyZone(config, row, domainsAdded)

    return domainsAdded

# create zone file if empty
def createEmptyZone(config, row, domainsAdded):
    if not os.path.isfile(config.master_zonePath + "/id" + str(row[0]) + ".zone"):
        domainsAdded = domainsAdded + 1
        f = open(config.master_zonePath + "/id" + str(row[0]) + ".zone", "w")
        f.write("""$TTL 3H
@   IN SOA  """ + config.master_hostname + """. """ + config.master_abuseAddress + """. (
                0   ; serial
                14400  ; refresh
                3600  ; retry
                1W  ; expire
                3H )    ; minimum""")
        f.close()

        logging.info("New domain " + str(row[1]) + " with ID " + str(row[0]) + " added!")

        return domainsAdded

# recreate the bind config in case of domain additions
def rewriteConfig(config):
    domainsRaw = listDomains()

    f = open(config.master_bindPath, "a")
    for row in domainsRaw:
        if row != None:
            if str(row[6]) == "1":
                f.write('''zone "''' + row[1] + '''" IN {
        type master;
        file "''' + config.master_zonePath + "/id" + row[0] + ".zone" + '''";
};''')

    f.close()

    return True



# run daemon function (main function)
def runDaemon(config):
    # local vars
    retryError = False

    # run the updateConfiguration once before start
    logging.info("Updating configuration on-start..")
    domainsAdded = updateConfiguration(config)
    logging.info("Configuration update completed.")
    logging.info(str(domainsAdded) + " new domains was added into the system.")

    # watchdog is used to capture the file change event
    class MyHandler(FileSystemEventHandler):
        def on_modified(self, event):
            logging.info("Update detected - updating configuration..")
            domainsAdded = updateConfiguration(config)
            logging.info("Configuration update completed.")
            logging.info(str(domainsAdded) + " new domains was added into the system.")

            # if new domains were added into the system
            if domainsAdded != 0 or retryError = True:
                logging.info("Rewriting bind configuration..")
                if rewriteConfig():
                    logging.info("Bind configuration update succesful!")
                    retryError = False
                else:
                    logging.error("Unable to perform configuration update!")
                    logging.error("daemon will retry on next update")

                    retryError = True

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path="/home/master-nafsdm/data", recursive=False)
    observer.start()

    logging.info("Daemon started!")
    try:
        while True:
            time.sleep(int(config.check_interval))
    except KeyboardInterrupt:
        # this is for the users who are debugging by just running the executable, we still catch the gracefulExits
        observer.stop()
    observer.join()
