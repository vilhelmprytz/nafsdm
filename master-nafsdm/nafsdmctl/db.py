# nafsdmctl
# db
# database functions for nafsdmctl
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

import sqlite3

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

def addDomain(sysArg):
    connection, cursor = dbConnection()

    format_str = """
INSERT INTO domain (id, domain, masterIP, comment, assignedNodes, dnssec, zoneManaged)
VALUES (NULL, "{domain}", "{masterIP}", "{comment}", "{assignedNodes}", "{dnssec}", 0);"""

    if sysArg[6] == "dnssec.no":
        dnssec = "n"
    elif sysArg[6] == "dnssec.yes":
        dnssec = "y"
    else:
        print("syntax error: invalid dnssec")

    sql_command = format_str.format(domain=sysArg[2], masterIP=sysArg[3], comment=sysArg[4], assignedNodes = sysArg[5], dnssec = dnssec)
    cursor.execute(sql_command)

    # close connection
    connection.commit()
    connection.close()

def removeDomain(domain):
    connection, cursor = dbConnection()

    sql_command = '''DELETE FROM domain WHERE domain="''' + domain + '''";'''

    # execute
    cursor.execute(sql_command)

    # check if domain is there
    cursor.execute('''SELECT * FROM domain WHERE domain= "''' + domain + '''";''')

    if len(cursor.fetchall()) == 0:
        status = True
    else:
        status = False

    # close connection
    connection.commit()
    connection.close()

    return status

def removeDomainId(domainId):
    connection, cursor = dbConnection()

    sql_command = '''DELETE FROM domain WHERE id="''' + str(domainId) + '''";'''

    # execute
    cursor.execute(sql_command)

    # check if domain is there
    cursor.execute('''SELECT * FROM domain WHERE id= "''' + str(domainId) + '''";''')

    if len(cursor.fetchall()) == 0:
        status = True
    else:
        status = False

    # close connection
    connection.commit()
    connection.close()

    return status

def listDomains():
    connection, cursor = dbConnection()

    cursor.execute("SELECT * FROM domain")
    result = cursor.fetchall()

    return result

def editDomain(domain, masterIP, comment, assignedNodes, dnssec):
    connection, cursor = dbConnection()

    # find the domain the user asked for
    sql_command = '''
SELECT * FROM domain
WHERE domain = "''' + domain + '''";'''

    cursor.execute(sql_command)
    result = cursor.fetchall()

    # check if we get valid reply
    if len(result) == 0:
        print("nafsdmctl: invalid domain")
        return False

    format_str = '''
UPDATE domain
SET masterIP = "{masterIP}", comment = "{comment}", assignedNodes = "{assignedNodes}", dnssec = "{dnssec}"
WHERE domain = "''' + domain + '''";'''

    if masterIP == None:
        masterIP = result[0][2]
    if comment == None:
        comment = result[0][3]
    if assignedNodes == None:
        assignedNodes = result[0][4]
    if dnssec == None:
        dnssec = result[0][5]

    sql_command = format_str.format(masterIP=masterIP, comment=comment, assignedNodes=assignedNodes, dnssec = dnssec)

    # execute update
    cursor.execute(sql_command)

    # close connection
    connection.commit()
    connection.close()

    return True

# update a certain column on certain domain
def setIntValue(row, column, value):
    # open up sql connection
    connection = sqlite3.connect("/home/master-nafsdm/data/domains.sql")
    cursor = connection.cursor()

    sql_command = """UPDATE domain
SET """ + str(column) + """ = """ + str(value) + """
WHERE domain = '""" + row + """';"""
    # execute
    cursor.execute(sql_command)

    # close connection
    connection.commit()
    connection.close()
