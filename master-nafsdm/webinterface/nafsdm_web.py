# nafsdm webinterface
# nafsdm_web.py
# main file for the flask engine behind the nafsdm webinterface

###########
## SETUP ##
###########

# imports
import logging
import sys
from logPath import logPath
from database import *

# flask setup
from flask import Flask
from flask import render_template, url_for, make_response, redirect, request, Response, flash
from functools import wraps


app = Flask(__name__)

# functions
def check_auth(username, password):
    #f = open("/var/www/portal/portalpassword.config")
    #passwordRaw = f.read()
    #f.close()

    return username == "admin" and password == "test"

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
    return render_template("404.html"), 404

@app.errorhandler(500)
def error_500(e):
    return render_template("500.html"), 500

#################
## MAIN ROUTES ##
#################
@app.route("/")
@requires_auth
def index():
    domains = []
    domainsRaw = listDomains()
    for domain in domainsRaw:
        if domain[5] == "y":
            domain[5] == "Enabled"
        elif domain[5] == "n":
            domain[5] == "Disabled"

        oneDomain = [domain[0], domain[1], domain[2], domain[3], domain[4], domain[5]]
        domains.append(oneDomain)
    return render_template("index.html", domains=domains)

################
## API ROUTES ##
################
