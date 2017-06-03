# nafsdmctl
# __main__
# main file for the nafsdmctl

# imports
import sys

# global vars
longLine = ("---------------------------------------------------------")

# global check if user hasn't typed any vars
if len(sys.argv) < 2:
    # length is two as len doesn't use 0 as first one
    print("syntax error: please use correct argument." + "\n" +
    "\n" + "nafsdmctl 'add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes'" +
    "\n" + "nafsdmctl 'remove domain.tld'" +
    "\n" + "nafsdmctl 'list'")
    exit(1)

# check which command user has run
if (sys.argv[1] == "add"):
    # syntax: nafsdmctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes
    if len(sys.argv) >= 6:
        # see if a there is a dot in first arg
        if ("." in sys.argv[2]):
            # check if there is four dots in the IP
            if (len(sys.argv[3].split(".")) == 4):
                f = open("/home/master-nafsdm/data/domains.txt", "a")
                f.write(sys.argv[2] + " " + sys.argv[3] + "" + sys.argv[4] + "" + sys.argv[5])
                f.close()
            else:
                print("syntax error: invalid master IP?")
                exit(1)
        else:
            print("syntax error: invalid domain name?")
            exit(1)
    else:
        print("syntax error: 'nafsdmctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes' is correct syntax")
        exit(1)
elif (sys.argv[1] == "remove"):
    # adding soon
    print("coming soon")
elif (sys.argv[1] == "list"):
    # read data
    f = open("/home/master-nafsdm/data/domains.txt")
    rawDomains = f.read()
    f.close()

    # parse & print data
    print("All current active domains:")
    print("domain.tld - masterIP - comment - assignedSlaves")
    print(longLine)

    for currentLine in rawDomains.split("\n"):
        allParameters = currentLine.split()
        print(allParameters[0] + " - " + allParameters[1] + " - " + allParameters[2] + " - " + allParameters[3])

    print(longLine)
else:
    # just prints some of the syntaxes and exists as an error
    print("syntax error: please use correct argument." + "\n" + 
    "\n" + "nafsdmctl 'add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes'" +
    "\n" + "nafsdmctl 'remove domain.tld'" +
    "\n" + "nafsdmctl 'list'")
    exit(1)
