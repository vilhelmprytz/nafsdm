# nafsdm
# help script for setting up nafsdm on the master
# Copyright Vilhelm Prytz 2017

# check if user is root or not
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run with root privileges (sudo)." 1>&2
  exit 1
fi

GITHUB_URL="https://github.com/MrKaKisen/nafsdm.git"
GITHUB_DIR="master-nafsdm"
HOME_DIR="/home/master-nafsdm"
USER="master-nafsdm"

echo "###################################################################"
echo "THIS SCRIPT WILL NOT WORK FOR UPDATING YOUR INSTALLATION"
echo "Welcome to nafsdm master install! Please enter your package manager (apt or yum only supported)."
echo -n "Package manager: "
read PACKAGEMAN

if [ "$PACKAGEMAN" == "yum" ]; then
  echo "Installing packages.. (NOTE: ROOT PASSW)"
  yum update -y
  yum install python python-pip git -y

  pip install requests
elif [ "$PACKAGEMAN" == "apt" ]; then
  echo "Installing packages.."
  apt-get update -y
  apt-get install python python-pip git -y

  pip install requests
else
  echo "Invalid package manager. Only apt and yum supported."
  exit 1
fi

echo "Required packages installed!"
echo "Downloading nafsdm & installing.."

# download in temp dir
cd /tmp
git clone $GITHUB_URL

useradd $USER
mkdir $HOME_DIR
mkdir $HOME_DIR/.ssh
chown -R master-nafsdm:master-nafsdm $HOME_DIR/.ssh
cp /tmp/nafsdm/$GITHUB_DIR /home -R
cp /tmp/nafsdm/LICENSE $HOME_DIR/LICENSE

cp /tmp/nafsdm/systemconfigs/nafsdmctl /usr/bin/nafsdmctl
cp /tmp/nafsdm/systemconfigs/nafsdm-master /usr/bin/nafsdm-master

chmod +x /usr/bin/nafsdmctl
chmod +x /usr/bin/nafsdm-master

echo "Installed. Cleanup.."

rm /tmp/nafsdm -rf

echo "To continue, please run 'nafsdm-master' for first time setup."
