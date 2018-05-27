# nafsdm webinterface
# nafsdm_web.py
# main file for the database connection
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

def addDomain(domain, masterIP, comment, assignedNodes, dnssec):
    connection, cursor = dbConnection()

    format_str = """
INSERT INTO domain (id, domain, masterIP, comment, assignedNodes, dnssec)
VALUES (NULL, "{domain}", "{masterIP}", "{comment}", "{assignedNodes}", "{dnssec}");"""

    if dnssec == "no":
        dnssecAdd = "n"
    elif dnssec == "yes":
        dnssecAdd = "y"
    else:
        print("syntax error: invalid dnssec")

    sql_command = format_str.format(domain=domain, masterIP=masterIP, comment=comment, assignedNodes=assignedNodes, dnssec=dnssecAdd)
    cursor.execute(sql_command)

    # close connection
    connection.commit()
    connection.close()

def removeDomain(domainId):
    connection, cursor = dbConnection()

    sql_command = '''DELETE FROM domain WHERE id="''' + domainId + '''";'''

    # execute
    cursor.execute(sql_command)

    # check if domain is there
    cursor.execute('''SELECT * FROM domain WHERE id= "''' + domainId + '''";''')

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

def editDomain(domainId, domain, masterIP, comment, assignedNodes, dnssec):
    connection, cursor = dbConnection()

    # find the domain the user asked for
    sql_command = '''
SELECT * FROM domain
WHERE id = "''' + domainId + '''";'''

    cursor.execute(sql_command)
    result = cursor.fetchall()

    # check if we get valid reply
    if len(result) == 0:
        print("nafsdmctl: invalid domain")
        return False

    format_str = '''
UPDATE domain
SET masterIP = "{masterIP}", comment = "{comment}", assignedNodes = "{assignedNodes}", dnssec = "{dnssec}"
WHERE id = "''' + domainId + '''";'''

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

def getStatistics():
    connection, cursor = dbConnection()
    sql_command = '''SELECT COUNT(*) FROM domain;'''

    # execute update
    cursor.execute(sql_command)
    result = cursor.fetchall()

    # close connection
    connection.commit()
    connection.close()

    # return result
    return result
