# nafsdm
# setup
# masterd setup functions

# imports
import subprocess
from daemonlog import log
import os, random, string
import sqlite3

# unused function, but will leave in here if it will be needed
def generatePassword(length=30):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    return(''.join(random.choice(chars) for i in range(length)))

def setupSSH():
    #generatedPassword = generatePassword()
    try:
        output = subprocess.check_output(["ssh-keygen", "-b", "4096", "-t", "rsa", "-f", "/home/master-nafsdm/.ssh/nafsdm_rsa", "-q", "-C", "nafsdm_master", "-N", ""])
        output = subprocess.check_output(["cp", "/home/master-nafsdm/.ssh/nafsdm_rsa.pub", "/home/master-nafsdm/.ssh/authorized_keys"])
    except Exception, e:
        log("FATAL: Some error ocurred during SSH key generation.")

    log("To continue, please copy /home/master-nafsdm/.ssh/nafsdm_rsa to all slaves /home/slave-nafsdm/.ssh/master_key")
    exit(1)

# SQL prepare
def setupDatabase():
    # setup DB connection
    connection = sqlite3.connect("/home/master-nafsdm/data/domains.sql")
    cursor = connection.cursor()

    # command to setup the table
    create_table_cmd = """
CREATE TABLE domain (
id INTEGER PRIMARY KEY,
domain VARCHAR(255),
masterIP VARCHAR(15),
comment TEXT,
assignedNodes TEXT,
dnssec CHAR(1));"""

    # execute the command
    cursor.execute(create_table_cmd)

    # close connection
    connection.commit()
    connection.close()

    log("Database & table created!")

# migrate data from domains.txt to domains.sql
def migrateData():
    # start with creating table
    setupDatabase()

    # read the old data
    f = open("/home/master-nafsdm/data/domains.txt")
    oldDomainsRaw = f.read()
    f.close()

    domainsTable = []

    # put it into a table
    for domain in oldDomainsRaw.split("\n"):
        if len(domain.split()) == 5:
            domainVars = domain.split()
            if domainVars[4] == "dnssec.yes":
                domainsTable.append(domainVars[0], domainVars[1], domainVars[2], domainVars[3], "y")
            elif domainVars[4] == "dnssec.no":
                domainsTable.append(domainVars[0], domainVars[1], domainVars[2], domainVars[3], "n")

    # open up sql connection
    connection = sqlite3.connect("/home/master-nafsdm/data/domains.sql")
    cursor = connection.cursor()

    # format the info from the table above into a sql command
    for addDomain in domainsTable:
        format_str = """INSERT INTO domain (id, domain, masterIP, comment, assignedNodes, dnssec)
VALUES (NULL, "{domain}", "{masterIP}", "{comment}", "{assignedNodes}", "{dnssec}");"""

        sql_command = format_str.format(domain=addDomain[0], masterIP=addDomain[1], comment=addDomain[2], assignedNodes = addDomain[3], dnssec = addDomain[4])
        cursor.execute(sql_command)

    # close connection
    connection.commit()
    connection.close()

    log("Migration complete. Deleting old domains.txt file.")

    os.remove("/home/master-nafsdm/data/domains.txt")

    log("Done.")
