# nafsdm
# daemonlog
# has logging functions
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

from time import strftime

def log(log):
    # write it to a file with current time / date
    write = "MANAGER " + strftime("%a, %d %b %Y %H:%M:%S") + " - " + log + "\n"

    f = open("/home/master-nafsdm/log.log", "a")
    f.write(write)
    f.close()

    # as systemd is used, we also print it (but without time/date)
    print(log)
