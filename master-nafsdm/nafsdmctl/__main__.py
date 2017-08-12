# nafsdmctl
# __main__
# main file for the nafsdmctl

# imports
import sys
import os
import os.path

# global vars
longLine = ("---------------------------------------------------------")

# global check if user hasn't typed any vars
if len(sys.argv) < 2:
    # length is two as len doesn't use 0 as first one
    print("syntax error: please use correct argument." + "\n" +
    "\n" + "nafsdmctl 'add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes'" +
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
                        f = open("/home/master-nafsdm/data/domains.txt", "a")
                        f.write(sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4] + " " + sys.argv[5] + " " + sys.argv[6] + "\n")
                        f.close()
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
            f = open("/home/master-nafsdm/data/domains.txt")
            rawDomains = f.read()
            f.close()

            # remove config
            os.remove("/home/master-nafsdm/data/domains.txt")

            wasRemoved = False
            for currentLine in rawDomains.split("\n"):
                if len(currentLine.split()) == 5:
                    if sys.argv[2] in currentLine:
                        wasRemoved = True
                    else:
                        f = open("/home/master-nafsdm/data/domains.txt", "a")
                        f.write(currentLine + "\n")
                        f.close()

            if wasRemoved == True:
                print("nafsdmctl: remove succesful")
            if wasRemoved == False:
                print("nafsdmctl: remove failed - invalid domain name?")
        else:
            print("syntax error: invalid domain name?")
    else:
        print("syntax error: 'nafsdmctl remove domain.tld' is correct syntax")
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
        print(currentLine)

    print(longLine)
elif (sys.argv[1] == "edit"):
    if (len(sys.argv) == 3):
        if "." in sys.argv[2]:
            f = open("/home/master-nafsdm/data/domains.txt")
            rawDomains = f.read()
            f.close()

            # remove config
            os.remove("/home/master-nafsdm/data/domains.txt")

            # fixing issue #11 by first checking if domain is there then editing
            wasFound = False
            for currentLine in rawDomains.split("\n"):
                if len(currentLine.split()) == 5:
                    if sys.argv[2] in currentLine:
                        f = open("/home/master-nafsdm/data/domains.txt", "a")
                        f.write(currentLine + "\n")
                        f.close()

                        wasFound = True
                    else:
                        f = open("/home/master-nafsdm/data/domains.txt", "a")
                        f.write(currentLine + "\n")
                        f.close()

            if wasFound == True:
                # domain name
                domain_name = raw_input("Enter new domain name (blank for no change): ")
                if domain_name == "":
                    domain_name = False

                # master IP
                master_ip = raw_input("Enter new master IP (blank for no change): ")
                if master_ip == "":
                    master_ip = False

                # comment
                comment = raw_input("Enter new comment (blank for no change): ")
                if comment == "":
                    comment = False

                # slaves
                slaves = raw_input("Enter new slaves (seperated with '.') (blank for no change): ")
                if "." in slaves:
                    if slaves == "":
                        slaves = False
                else:
                    print("syntax error: invalid slaves. Continuing anyways (set to same as before)")
                    slaves = False

                # DNSSEC
                dnssec = raw_input("Edit DNSSEC status (only type yes or no) (blank for no change): ")
                if dnssec == "yes":
                    dnssec = "dnssec.yes"
                elif dnssec == "no":
                    dnssec = "dnssec.no"
                else:
                    dnssec = False
                    print("syntax error: only yes or no supported. Value set to same as before.")
            else:
                print("nafsdmctl: edit failed - domain name not found?")
                exit(1)

            # remove config
            os.remove("/home/master-nafsdm/data/domains.txt")

            wasEdited = False
            for currentLine in rawDomains.split("\n"):
                if len(currentLine.split()) == 5:
                    if sys.argv[2] in currentLine:

                        if domain_name == False:
                            domain_name = currentLine.split()[0]
                        if master_ip == False:
                            master_ip = currentLine.split()[1]
                        if comment == False:
                            comment = currentLine.split()[2]
                        if slaves == False:
                            slaves = currentLine.split()[3]
                        if dnssec == False:
                            dnssec = currentLine.split()[4]

                        writeLine = domain_name + " " + master_ip + " " + comment + " " + slaves + " " + dnssec + "\n"
                        f = open("/home/master-nafsdm/data/domains.txt", "a")
                        f.write(writeLine)
                        f.close()

                        wasEdited = True
                    else:
                        f = open("/home/master-nafsdm/data/domains.txt", "a")
                        f.write(currentLine + "\n")
                        f.close()

            if wasEdited == True:
                print("nafsdmctl: edit succesful")
            if wasEdited == False:
                print("nafsdmctl: edit failed - this has probably destroyed your config!")
        else:
            print("syntax error: invalid domain name?")
    else:
        print("syntax error: 'nafsdmctl edit domain.tld' is correct syntax")
else:
    # just prints some of the syntaxes and exists as an error
    print("syntax error: please use correct argument." + "\n" +
    "\n" + "nafsdmctl 'nafsdmctl add domain.tld 0.0.0.0 OwnComment nodes.nodes.nodes dnssec.[yes/no]'" +
    "\n" + "nafsdmctl 'remove domain.tld'" +
    "\n" + "nafsdmctl 'list'")
    exit(1)
