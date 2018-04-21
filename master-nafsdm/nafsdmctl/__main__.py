# nafsdmctl
# __main__
# main file for the nafsdmctl
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import sys
import os
import os.path
from tabulate import tabulate
from db import *
from connAlive import slaveConnections
import subprocess
import time

# catching ctrl+c
import signal

# global vars
debug = False
class bcolors: # (thanks to https://stackoverflow.com/a/287944/8321546)
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    # thanks to https://stackoverflow.com/questions/287871/print-in-terminal-with-colors/287944#comment7475474_287944
    BOLD = "\033[1m"
    # thanks to https://stackoverflow.com/a/21786287/8321546
    GREENBG = "\x1b[6;30;42m" # green bg with black text
    REDBG = "\x1b[2;30;41m" # red bg with black text

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

# functions
def signal_handler(signal, frame):
    print("CTRL+C - quitting.")
    exit(0)

# visual print functions
def errorPrint(message):
    print("nafsdmctl: " + bcolors.FAIL + message + bcolors.ENDC)

def successPrint(message):
    print("nafsdmctl: " + bcolors.OKGREEN + message + bcolors.ENDC)

def printSyntax():
    # syntax and info
    print("Usage: nafsdmctl [COMMAND] [ARG] ...")
    print("\n" + bcolors.BOLD + bcolors.FAIL + "nafsdm control " + bcolors.ENDC + "for master daemon" + "\n")
    print("Commands:")
    print(bcolors.BOLD + " slavestatus" + bcolors.ENDC + "                                                     Shows connection status of all slaves.")
    print(bcolors.BOLD + " add [domain] [masterIP] [comment] [nodes.nodes] [dnssec.no/yes]" + bcolors.ENDC + " Add a new domain")
    print(bcolors.BOLD + " removedomain [domain]" + bcolors.ENDC + "                                           Remove a record by domain")
    print(bcolors.BOLD + " removeid [id]" + bcolors.ENDC + "                                                   Remove a record by ID")
    print(bcolors.BOLD + " edit [domain]" + bcolors.ENDC + "                                                   Edit a domain")
    print(bcolors.BOLD + " list" + bcolors.ENDC + "                                                            List all domains")
    print("\n" + "nafsdm webinterface commands:")
    print(bcolors.BOLD + " webinterface status" + bcolors.ENDC + "                                             Shows status of webinterface")
    print(bcolors.BOLD + " webinterface start" + bcolors.ENDC + "                                              Start the nafsdm-webinterface")
    print(bcolors.BOLD + " webinterface stop" + bcolors.ENDC + "                                               Start the nafsdm-webinterface")
    print(bcolors.BOLD + " webinterface restart" + bcolors.ENDC + "                                            Start the nafsdm-webinterface")

# webinterface control commands
def webinterfaceStatus():
    try:
        output = subprocess.check_output(["/bin/systemctl", "status", "nafsdm-webinterface.service"])
    except Exception, e:
        outputSaved = str(e.output)
        if debug:
            print("DEBUG - output from systemctl status nafsdm-webinterface")
            print(outputSaved)
        for line in outputSaved.split("\n"):
            if "Active:" in line:
                if "active (running)" in line:
                    return True
                else:
                    return False
        errorPrint("an error occured during status check (perhaps webinterface is not enabled on this system?)")
        exit(1)

    for line in output.split("\n"):
        if "Active:" in line:
            if "active (running)" in line:
                return True
    # systemd should give us 'Active: active (running)' if it's running, otherwise it's not
    return False

def startWebinterface():
    # simple start command to systemd
    try:
        output = subprocess.check_output(["/bin/systemctl", "start", "nafsdm-webinterface.service"])
    except Exception:
        errorPrint("an error occured during webinterface start")
        exit(1)

    return True
def stopWebinterface():
    # simple stop command to systemd
    try:
        output = subprocess.check_output(["/bin/systemctl", "stop", "nafsdm-webinterface.service"])
    except Exception:
        errorPrint("an error occured during webinterface stop")
        exit(1)

    return True

def restartWebinterface():
    # we'll send a simple restart command to systemd
    try:
        output = subprocess.check_output(["/bin/systemctl", "restart", "nafsdm-webinterface.service"])
    except Exception:
        errorPrint("an error occured during webinterface restart")
        exit(1)

    return True

# slave connection status
def printSlaveConnections():
    # get slave connection status
    slaveConn = slaveConnections(bcolors)

    # print a fancy table using tabulate
    headers = [bcolors.BOLD + "hostname", "latest connection", "latest connection date", "interval" + bcolors.ENDC]

    print(bcolors.BOLD + "Current date: " + bcolors.ENDC + time.strftime("%Y-%M-%d %H:%M:%S") + "\n")
    print tabulate(slaveConn, headers, tablefmt="fancy_grid")

# global check if user hasn't typed any vars
if len(sys.argv) < 2:
    # not enough args
    printSyntax()
    exit(0)

# check which command user has run
if (sys.argv[1] == "add"):
    # syntax: nafsdmctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes dnssec.[yes/no]
    if len(sys.argv) >= 7:
        # see if a there is a dot in first arg
        if ("." in sys.argv[2]):
            # check if there is four dots in the IP
            if (len(sys.argv[3].split(".")) == 4):
                if "." in sys.argv[6]:
                    if "yes" in sys.argv[6] or "no" in sys.argv[6]:
                        addDomain(sys.argv)
                        successPrint("domain added")
                    else:
                        errorPrint("use dnssec.yes or dnssec.no only.")
                        exit(1)
                else:
                    errorPrint("invalid dnssec option")
                    exit(1)
            else:
                errorPrint("invalid master IP")
                exit(1)
        else:
            errorPrint("invalid domain name")
            exit(1)
    else:
        errorPrint("not enough arguments")
        printSyntax()
        exit(1)
elif (sys.argv[1] == "removedomain"):
    if (len(sys.argv) == 3):
        if "." in sys.argv[2]:
            if removeDomain(sys.argv[2]) == True:
                successPrint("remove succesful")
            else:
                errorPrint("remove failed - invalid domain name?")
        else:
            errorPrint("invalid domain name")
    else:
        errorPrint("not enough arguments")
        printSyntax()
        exit(1)
elif (sys.argv[1] == "removeid"):
    if (len(sys.argv) == 3):
        if removeDomainId(sys.argv[2]) == True:
            successPrint("remove succesful")
        else:
            errorPrint("remove failed - invalid id?")
    else:
        errorPrint("not enough arguments")
        printSyntax()
        exit(1)
elif (sys.argv[1] == "list"):
    # get domains
    domainsRaw = listDomains()

    # create table we append domains in
    printTable = []

    for row in domainsRaw:
        if row != None:
            if row[5] == "y":
                printTable.append([str(row[0]), row[1], row[2], row[3], row[4], bcolors.OKGREEN + "yes" + bcolors.ENDC])
            elif row[5] == "n":
                printTable.append([str(row[0]), row[1], row[2], row[3], row[4], bcolors.FAIL + "no" + bcolors.ENDC])
            else:
                printTable.append([str(row[0]), row[1], row[2], row[3], row[4], row[5]])

    # print a fancy table using tabulate
    headers = [bcolors.BOLD + "id", "domain", "master IP", "comment", "slaves", "DNSSEC status" + bcolors.ENDC]
    print tabulate(printTable, headers, tablefmt="fancy_grid")


elif (sys.argv[1] == "edit"):
    if (len(sys.argv) == 3):
        if "." in sys.argv[2]:
            # master IP
            master_ip = raw_input("Enter new master IP (blank for no change): ")
            if master_ip == "":
                master_ip = None

            # comment
            comment = raw_input("Enter new comment (blank for no change): ")
            if comment == "":
                comment = None

            # slaves
            slaves = raw_input("Enter new slaves (seperated with '.') (blank for no change): ")
            if "." in slaves:
                if slaves == "":
                    slaves = None
            else:
                errorPrint("invalid slaves. Continuing anyways (value set to same as before)")
                slaves = None

            # DNSSEC
            dnssec = raw_input("Edit DNSSEC status (only type yes or no) (blank for no change): ")
            if dnssec == "yes":
                dnssec = "y"
            elif dnssec == "no":
                dnssec = "n"
            else:
                dnssec = None
                errorPrint("only yes or no supported. Value set to same as before.")

            # set the domain
            domain = sys.argv[2]

            if editDomain(domain, master_ip, comment, slaves, dnssec) == True:
                successPrint("edit succesful")
            else:
                errorPrint("edit failed")
        else:
            errorPrint("invalid domain name?")
    else:
        errorPrint("not enough arguments")
        printSyntax()
        exit(1)
elif (sys.argv[1] == "webinterface"):
    if len(sys.argv) < 3:
        errorPrint("not enough arguments")
        printSyntax()
        exit(1)
    else:
        if sys.argv[2] == "status":
            if webinterfaceStatus():
                print("status: " + bcolors.GREENBG + "running" + bcolors.ENDC)
            else:
                print("status: " + bcolors.REDBG + "not running" + bcolors.ENDC)
        elif sys.argv[2] == "start":
            if webinterfaceStatus():
                errorPrint("webinterface is already running")
            else:
                if startWebinterface():
                    successPrint("webinterface started")
        elif sys.argv[2] == "stop":
            if stopWebinterface():
                successPrint("webinterface stopped")
        elif sys.argv[2] == "restart":
            if restartWebinterface():
                successPrint("webinterface restarted")
        else:
            errorPrint("invalid webinterface argument")
            printSyntax()
            exit(1)
elif (sys.argv[1] == "slavestatus"):
    printSlaveConnections()
else:
    printSyntax()
    exit(1)
