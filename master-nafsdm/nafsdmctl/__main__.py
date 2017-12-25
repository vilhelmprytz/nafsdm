# nafsdmctl
# __main__
# main file for the nafsdmctl

# imports
import sys
import os
import os.path
import db

# catching ctrl+c
import signal
import sys

# global vars
longLine = ("---------------------------------------------------------")

# functions
def signal_handler(signal, frame):
    print("CTRL+C - quitting.")
    exit(0)

# global check if user hasn't typed any vars
if len(sys.argv) < 2:
    # length is two as len doesn't use 0 as first one
    print("syntax error: please use correct argument." + "\n" +
    "\n" + "nafsdmctl 'add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes dnssec.[yes/no]'" +
    "\n" + "nafsdmctl 'remove domain.tld'" +
    "\n" + "nafsdmctl 'edit domain.tld'"+
    "\n" + "nafsdmctl 'list'")
    exit(1)

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
                        print("Domain added.")
                    else:
                        print("syntax error: use dnssec.yes or dnssec.no only.")
                else:
                    print("syntax error: invalid dnssec option?")
            else:
                print("syntax error: invalid master IP?")
                exit(1)
        else:
            print("syntax error: invalid domain name?")
            exit(1)
    else:
        print("syntax error: 'nafsdmctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes dnssec.[yes/no]' is correct syntax")
        exit(1)
elif (sys.argv[1] == "remove"):
    if (len(sys.argv) == 3):
        if "." in sys.argv[2]:
            if removeDomain(sys.argv[2]) == True:
                print("nafsdmctl: remove succesful")
            else:
                print("nafsdmctl: remove failed. Invalid domain name?")
        else:
            print("syntax error: invalid domain name?")
    else:
        print("syntax error: 'nafsdmctl remove domain.tld' is correct syntax")
elif (sys.argv[1] == "list"):
    listDomains()
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
                print("syntax error: invalid slaves. Continuing anyways (set to same as before)")
                slaves = None

            # DNSSEC
            dnssec = raw_input("Edit DNSSEC status (only type yes or no) (blank for no change): ")
            if dnssec == "yes":
                dnssec = "y"
            elif dnssec == "no":
                dnssec = "n"
            else:
                dnssec = None
                print("syntax error: only yes or no supported. Value set to same as before.")

            if editDomain(domain, master_ip, comment, slaves, dnssec) == True:
                print("nafsdmctl: edit succesful")
            else:
                print("nafsdmctl: edit failed")
        else:
            print("syntax error: invalid domain name?")
    else:
        print("syntax error: 'nafsdmctl edit domain.tld' is correct syntax")
else:
    # just prints some of the syntaxes and exists as an error
    print("syntax error: please use correct argument." + "\n" +
    "\n" + "nafsdmctl 'nafsdmctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes dnssec.[yes/no]'" +
    "\n" + "nafsdmctl 'remove domain.tld'" +
    "\n" + "nafsdmctl 'edit domain.tld'"+
    "\n" + "nafsdmctl 'list'")
    exit(1)
