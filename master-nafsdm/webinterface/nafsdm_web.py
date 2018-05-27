# nafsdm webinterface
# nafsdm_web.py
# main file for the flask engine behind the nafsdm webinterface
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

###########
## SETUP ##
###########

# imports
import logging
import sys
import subprocess
import os
import platform
from versionCheck import *
from logPath import logPath
from database import *
from connAlive import *
from time import gmtime, strftime

# flask setup
from flask import Flask
from flask import render_template, url_for, make_response, redirect, request, Response, flash
from functools import wraps

# import master version
import sys
sys.path.insert(0, "/home/master-nafsdm/pythondaemon")
from version import version as masterVersion


app = Flask(__name__)

# functions
def check_auth(username, password):
    f = open("/home/master-nafsdm/webinterface/interfacePassword.txt")
    passwordRaw = f.read()
    f.close()

    if len(passwordRaw.split("\n")) == 2:
        passReturn = passwordRaw.split("\n")[0]
    elif len(passwordRaw.split("\n")) == 1:
        passReturn = passwordRaw.split("\n")[0]
    else:
        return "Invalid password in configuration", 500

    return username == "admin" and password == passReturn

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# setup logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# format for logger
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# add stdout to logger
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# add file handler to logger
fh = logging.FileHandler(logPath)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

logging.info("Welcome to nafsdm-master webinterface!")

####################
## ERROR HANDLERS ##
####################
@app.errorhandler(404)
def error_404(e):
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return render_template("404.html", version=masterVersion, date=date), 404

@app.errorhandler(500)
def error_500(e):
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return render_template("500.html", version=masterVersion, date=date), 500

#################
## MAIN ROUTES ##
#################
@app.route("/")
@requires_auth
def index():
    status, devIcMode, github_branch, myVersion, newestVersion = checkUpdate()
    if status:
        if devIcMode:
            if myVersion == newestVersion:
                versionColor = "green"
                versionMsg = "Running latest incremental commits update - version " + myVersion
            else:
                versionColor = "red"
                versionMsg = "Not running latest incremental commits update (latest version is " + newestVersion + ")"
        else:
            if myVersion == newestVersion:
                versionColor = "green"
                versionMsg = "Running latest version - version " + myVersion
            else:
                versionColor = "red"
                versionMsg = "Not running latest version (latest version is " + newestVersion + ")"
    else:
        versionMsg = "Unable to detect version (connection issues?)"

    # loadavg
    try:
        loadAvg = os.getloadavg()
    except Exception:
        loadAvg = "error"

    # get kernel version
    kernel = platform.platform()

    # Statistics
    domainsNumber = getStatistics()
    slavesNumber = int(slaveConnections())

    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return render_template("index.html", version=masterVersion, date=date, github_branch=github_branch, myVersion=myVersion, devIcMode=devIcMode, versionColor=versionColor, versionMsg=versionMsg, loadAvg=loadAvg, kernel=kernel, domainsNumber=domainsNumber, slavesNumber=slavesNumber)

@app.route("/domains")
@requires_auth
def domains():
    # get args
    remove = request.args.get("remove")
    add = request.args.get("add")
    addSuccess = request.args.get("addSuccess")
    removeSuccess = request.args.get("removeSuccess")
    fail = request.args.get("fail")
    editRaw = request.args.get("edit")
    editSuccess = request.args.get("editSuccess")

    try:
        edit = int(editRaw.split()[0])
    except Exception:
        edit = None

    domains = []
    domainsRaw = listDomains()
    for domain in domainsRaw:
        if domain[5] == "y":
            oneDomain = [domain[0], domain[1], domain[2], domain[3], domain[4], "Enabled", "y"]
        elif domain[5] == "n":
            oneDomain = [domain[0], domain[1], domain[2], domain[3], domain[4], "Disabled", "n"]
        else:
            oneDomain = [domain[0], domain[1], domain[2], domain[3], domain[4], domain[5], domain[5]]
        domains.append(oneDomain)

    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return render_template("domains.html", domains=domains, add=add, remove=remove, edit=edit, addSuccess=addSuccess, removeSuccess=removeSuccess, editSuccess=editSuccess, fail=fail, version=masterVersion, date=date)

@app.route("/slavestatus")
@requires_auth
def slavestatus():
    flushSuccess = request.args.get("flushSuccess")
    fail = request.args.get("fail")

    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    slaves = slaveConnections()
    return render_template("slavestatus.html", slaves=slaves, flushSuccess=flushSuccess, fail=fail, version=masterVersion, date=date)

################
## API ROUTES ##
################
@app.route("/api/newDomain", methods=["POST"])
@requires_auth
def api_newDomain():
    domain = request.form["domain"]
    masterIP = request.form["masterIP"]
    comment = request.form["comment"]
    assignedNodes = request.form["assignedNodes"]
    dnssec = request.form["dnssec"]

    addDomain(domain, masterIP, comment, assignedNodes, dnssec)

    return redirect("/domains?addSuccess=true")

@app.route("/api/removeDomain")
@requires_auth
def api_removeDomain():
    domainId = request.args.get("id")

    status = removeDomain(domainId)

    if status == True:
        return redirect("/domains?removeSuccess=true")
    else:
        return redirect("/domains?fail=true")

@app.route("/api/editDomain", methods=["POST"])
@requires_auth
def api_editDomain():
    domainId = request.form["id"]
    domain = request.form["domain"]
    masterIP = request.form["masterIP"]
    comment = request.form["comment"]
    assignedNodes = request.form["assignedNodes"]
    dnssec = request.form["dnssec"]

    status = editDomain(domainId, domain, masterIP, comment, assignedNodes, dnssec)

    if status == True:
        return redirect("/domains?editSuccess=true")
    else:
        return redirect("/domains?fail=true")

@app.route("/api/slaveFlush")
@requires_auth
def api_slaveFlush():
    if not flushSlaveConnections():
        return redirect("/slavestatus?flushSuccess=true")
    else:
        return redirect("/slavestatus?fail=true")
