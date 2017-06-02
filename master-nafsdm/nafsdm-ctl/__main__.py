# nafsdm-ctl
# __main__
# main file for the nafsdm-ctl

# imports
import sys

# global vars
longLine = ("---------------------------------------------------------")


# check which command user has run
if (sys.argv[0] == "add"):
    # syntax: nafsdm-ctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes
    if len(sys.argv) >= 5:
        # see if a there is a dot in first arg
        if ("." in sys.argv[1]):
            # check if there is four dots in the IP
            if (len(sys.argv[2].split(".")) == 4):
                f = open("/home/master-nafsdm/data/domains.txt", "a")
                f.write(sys.argv[1] + " " + sys.argv[2] + "" + sys.argv[3] + "" + sys.argv[4])
                f.close()
            else:
                print("syntax error: invalid master IP?")
                exit(1)
        else:
            print("syntax error: invalid domain name?")
            exit(1)
        else:
    else:
        print("syntax error: 'nafsdm-ctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes' is correct syntax")
        exit(1)
elif (sys.argv[0] == "remove"):
    # will add soon
elif (sys.argv[0] == "list"):
    # read data
    f = open("/home/master-nafsdm/data/domains.txt")
    rawDomains = f.read()
    f.close()

    # parse & print data
    print("All current active domains:")
    print("domain.tld - masterIP - comment - assignedSlaves")
    print(longLine)

    for currentLine in rawDomains.split("\n")
        allParameters = currentLine.split()
        print(allParameters[0] + " - " + allParameters[1] + " - " + allParameters[2] + " - " + allParameters[3])

    print(longLine)
else:
    # just prints some of the syntaxes and exists as an error
    print("syntax error: please use correct argument." +
    "\n" + "nafsdm-ctl 'add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes'" +
    "\n" + "nafsdm-ctl 'remove domain.tld'" +
    "\n" + "nafsdm-ctl 'list'")
    exit(1)
