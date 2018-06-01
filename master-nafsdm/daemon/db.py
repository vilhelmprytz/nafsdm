# nafsdm-master daemon
# db
# database communication
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

import sqlite3
import logging

# general db connection
def dbConnection():
    try:
        connection = sqlite3.connect("/home/master-nafsdm/data/domains.sql")
    except Exception:
        # if it can't connect to the file
        print("Could not read from domains.sql file! If this is the first time running, please run the master atleast once.")
        exit(1)

    cursor = connection.cursor()
    return connection, cursor

def listDomains():
    connection, cursor = dbConnection()

    cursor.execute("SELECT * FROM domain")
    result = cursor.fetchall()

    return result
