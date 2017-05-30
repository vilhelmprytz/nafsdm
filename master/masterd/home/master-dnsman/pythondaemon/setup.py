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
        output = subprocess.check_output(["ssh-keygen ", "-t", "rsa", "-b", "4096", "-C", "'DNS manager'", "-P", "'" + generatedPassword + "'", "-f", "'/home/master-dnsman/dns_manager_rsa'", "-q"])
    except Exception, e:
        print("Some error ocurred.")
