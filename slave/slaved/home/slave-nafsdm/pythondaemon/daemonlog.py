# nafsdm
# daemonlog
# log stuff

from time import strftime

def log(log):
    write = strftime("%a, %d %b %Y %H:%M:%S") + " - " + log + "\n"

    f = open("/home/slave-nafsdm/log.log", "a")
    f.write(write)
    f.close()
