# nafsdm
# (c) Vilhelm Prytz 2017
# daemonlog
# log stuff

from time import strftime

def log(log):
    # write it to a file with current time / date
    write = strftime("%a, %d %b %Y %H:%M:%S") + " - " + log + "\n"

    f = open("/home/slave-nafsdm/log.log", "a")
    f.write(write)
    f.close()

    # as systemd is used, we also print it (but without time/date)
    print(log)
