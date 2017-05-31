# dns-manager
# setup
# masterd setup functions

# imports
import subprocess
import os, random, string

def generatePassword(length=30):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    return(''.join(random.choice(chars) for i in range(length)))

def setupSSH():
    generatedPassword = generatePassword()
    try:
        output = subprocess.check_output(["mkdir", "/home/master-dnsman/.ssh"])
        output = subprocess.check_output(["ssh-keygen ", "-t", "rsa", "-b", "4096", "-C", "'DNS manager'", "-P", "'" + generatedPassword + "'", "-f", "'/home/master-dnsman/.ssh/dns_manager_rsa'", "-q"])
        output = subprocess.check_output(["cp", "/home/master-dnsman/.ssh/dns_manager_rsa.pub", "/home/master-dnsman/.ssh/authorized_keys"])
    except Exception, e:
        log("FATAL: Some error ocurred during SSH key generation.")

    log("To continue, please copy /home/master-dnsman/dns_manager_rsa to all slaves /home/slave-dnsman/.ssh/master_key")
    exit(0)
