# nafsdm
# (c) Vilhelm Prytz 2018
# db
# database SQL communication
# https://github.com/mrkakisen/nafsdm

import logging
import sqlite3

# vars
domains_beforePath = "/home/slave-nafsdm/temp/domain_before.sql"
domains_tempPath = "/home/slave-nafsdm/temp/domains_temp.sql"

# general db connection
def dbConnection(path):
    try:
        connection = sqlite3.connect(path)
    except Exception:
        logging.exception("Could not open SQL connection!")
        logging.error("DB connection failure - does the SQL file exist?")

        return None, None, False


    cursor = connection.cursor()
    return connection, cursor, True

# get and parse the data from all domains
def parseDbData(config):
    connection, cursor, connectionStatus = dbConnection(domains_tempPath)
    if connectionStatus == False:
        logging.error("Cannot parse data due to previous error.")
        return False
    else:
        # get all the nodes where we have our hostname in the assignedNodes
        cursor.execute('''SELECT * FROM domain
WHERE assignedNodes LIKE "%''' + config.nodeName +  '''%"''')

        result = cursor.fetchall()

        if len(result) == 0:
            return False

        return result
