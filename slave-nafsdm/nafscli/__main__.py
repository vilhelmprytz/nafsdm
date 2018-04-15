# nafscli
# __main__
# main file for the nafscli
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import sys
import os
import subprocess
import requests

# global vars
github_branch = "master"
debug = False
debugVersion = "1.2.3-stable"
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
def errorPrint(message):
    print("nafscli: " + bcolors.FAIL + message + bcolors.ENDC)

def successPrint(message):
    print("nafscli: " + bcolors.OKGREEN + message + bcolors.ENDC)

def printSyntax():
    # syntax and info
    print("Usage: nafscli [COMMAND]")
    print("\n" + bcolors.BOLD + bcolors.FAIL + "nafsdm command-line interface " + bcolors.ENDC + "for slave daemon" + "\n")
    print("Commands:")
    print(bcolors.BOLD + " status" + bcolors.ENDC + "      Show current status of the daemon")
    print(bcolors.BOLD + " version" + bcolors.ENDC + "     Current version of nafsdm")
    print(bcolors.BOLD + " restart" + bcolors.ENDC + "     Restart the daemon")
    print(bcolors.BOLD + " upgrade" + bcolors.ENDC + "     Upgrade the daemon")

def checkStatus():
    try:
        output = subprocess.check_output(["/bin/systemctl", "status", "nafsdm-slave.service"])
    except Exception:
        errorPrint("an error occured during status check")
        exit(1)

    for line in output.split():
        if "Active:" in line:
            if "active (running)" in line:
                return True
    # systemd should give us 'Active: active (running)' if it's running, otherwise it's not
    return False

def fetchVersion():
    try:
        f = open("/home/slave-nafsdm/version.py")
    except Exception:
        # if the file doesnt exist
        errorPrint("could not find daemon version file - is the daemon installed?")
        if debug:
            return debugVersion
        exit(1)
    versionRaw = f.read()
    f.close()

    try:
        # simple split sequence to divide the string into words, and then remove the quotation marks
        version = versionRaw.split()[2].split('"')[1]
    except Exception:
        errorPrint("could not determine daemon version")
        exit(1)

    return version

def checkVersion(currentVersion):
    r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/" + github_branch + "/version.txt")

    # check for ok response codes
    if (r.status_code == requests.codes.ok):
        # code borrowed from daemon/versionCheck.py
        if (r.text.split("\n")[0] == currentVersion):
            return True, None
        else:
            return False, r.text.split("\n")[0]

def restartDaemon():
    # we'll send a simple restart command to systemd
    try:
        output = subprocess.check_output(["/bin/systemctl", "restart", "nafsdm-slave.service"])
    except Exception:
        errorPrint("an error occured during daemon restart")
        exit(1)

    return True

# the CLI can communicate with the daemon by setting a new CLI state
def setCLIState(newState):
    if checkStatus():
        try:
            f = open("/home/slave-nafsdm/pythondaemon/cli_state", "w")
        except Exception:
            errorPrint("could not set CLI state")
            exit(1)

        f.write(newState)
        f.close()
    else:
        errorPrint("daemon is not running, cannot set CLI state")
# debug print
if debug:
    print("Debugg: " + str(sys.argv))

# syntax print
if len(sys.argv) < 2:
    printSyntax()
    exit(0)

# routes
if sys.argv[1] == "status":
    status = checkStatus()
    if status == True:
        print("status: " + bcolors.GREENBG + "running" + bcolors.ENDC)
    else:
        print("status: " + bcolors.REDBG + "not running" + bcolors.ENDC)

elif sys.argv[1] == "version":
    version = fetchVersion()
    versionStatus, newVersion = checkVersion(version)
    if versionStatus == True:
        print("nafscli: you're running the latest version, " + version)
    else:
        print("nafscli: " + bcolors.OKGREEN + "a new version is available, " + bcolors.BOLD + newVersion + bcolors.ENDC)
        print("         " + bcolors.OKGREEN + "upgrade using 'nafscli upgrade'" + bcolors.ENDC)
elif sys.argv[1] == "restart":
    if restartDaemon():
        successPrint("daemon restarted")
elif sys.argv[1] == "upgrade":
    setCLIState("upgrade")
    successPrint("upgrade command sent to daemon")
else:
    print("nafscli: " + bcolors.FAIL + "no such command '" + bcolors.BOLD + sys.argv[1] + "'" + bcolors.ENDC)
