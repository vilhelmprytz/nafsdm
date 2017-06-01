# nafsdm
# daemonlog
# has logging functions

from time import strftime

def log(log):
    write = strftime("%a, %d %b %Y %H:%M:%S") + " - " + log + "\n"

    f = open("/home/master-nafsdm/log.log", "a")
    f.write(write)
    f.close()
