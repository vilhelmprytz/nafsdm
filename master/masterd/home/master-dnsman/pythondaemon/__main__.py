# dns-manager
# __main__
# masterd startup file

# imports
import os.path
from setup import setupSSH


# check if first time
if not os.path.exists("/home/master-dnsman/.ssh"):
    
