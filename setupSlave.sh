# nafsdm
# help script for setting up nafsdm on all slaves
# Copyright Vilhelm Prytz 2017
# https://github.com/mrkakisen/nafsdm

# check if user is root or not
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run with root privileges (sudo)." 1>&2
  exit 1
fi

#  DL_VERSION will be changed at the time of update
DL_URL="https://github.com/MrKaKisen/nafsdm/archive/"
GITHUB_DIR="slave-nafsdm"
HOME_DIR="/home/slave-nafsdm"
USER="slave-nafsdm"

echo "###################################################################"
echo "* nafsdm-slave installation script"
echo "* note: this installer will not upgrade your installation"
echo "###################################################################"
echo "* Please enter your operating system name ('debian', 'ubuntu' and 'centos' only supported)"
echo -n "* Operating system: "
read OPERATINGSYS

if [ "$OPERATINGSYS" == "centos" ]; then
  echo "* Installing packages.."
  yum update -y
  yum install python curl wget -y

  # centos does not have pip in it's repos
  curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
  python get-pip.py
  rm get-pip.py -rf

  pip install requests
elif [[ "$OPERATINGSYS" == "debian" ]] || [[ "$OPERATINGSYS" == "ubuntu" ]] ; then
  echo "* Installing packages.."
  apt-get update -y
  apt-get install python python-pip curl wget -y

  pip install requests
else
  echo "* Invalid operating system. Only 'debian', 'ubuntu' and 'centos' supported."
  exit 1
fi

# get which version is the latest
echo "* Fetching information about latest version.."
LATEST_VERSION=$(curl https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/version.txt)

# select version
echo "* Please select your version. Type in the version number or type 'latest' for latest version."
echo -n "* Version: "
read VERSION_USER

if [ "$VERSION_USER" == "latest" ]; then
  echo -n "* Confirm? (y/n): "
  read CONFIRM
  if [ "$CONFIRM" == "y" ]; then
    DL_VERSION="$LATEST_VERSION"
  else
    echo "* Aborting.."
    exit 1
  fi
else
  echo -n "* Confirm? If version doesn't exist, script will fail. (y/n): "
  read CONFIRM
  if [ "$CONFIRM" == "y" ]; then
    DL_VERSION="$VERSION_USER"
  else
    echo "* Aborting.."
    exit 1
  fi
fi

echo "* Required packages installed!"
echo "* Downloading nafsdm & installing.."

# download in temp dir
cd /tmp
wget $DL_URL$DL_VERSION.tar.gz -O nafsdm.tar.gz
tar -zxvf nafsdm.tar.gz
mv nafsdm-* nafsdm

useradd $USER
# debian and ubuntu doesn't create its home dir automatically, unlike centos
if [[ "$OPERATINGSYS" == "debian" ]] || [[ "$OPERATINGSYS" == "ubuntu" ]] ; then
  mkdir $HOME_DIR
fi
mkdir $HOME_DIR/.ssh
chown -R slave-nafsdm:slave-nafsdm $HOME_DIR/.ssh
cp /tmp/nafsdm/$GITHUB_DIR /home -R
cp /tmp/nafsdm/$GITHUB_DIR/nafscli /home/$GITHUB_DIR/nafscli -R
cp /tmp/nafsdm/LICENSE $HOME_DIR/LICENSE

cp /tmp/nafsdm/systemconfigs/nafsdm-slave.service /etc/systemd/system/nafsdm-slave.service
cp /tmp/nafsdm/systemconfigs/nafscli /usr/bin/nafscli

# make service start upon boot
/usr/bin/env systemctl enable nafsdm-slave

chmod +x /home/slave-nafsdm/start.py
chmod +x /usr/bin/nafsdmctl

echo "* Installed. Cleanup.."

rm /tmp/nafsdm -rf

echo "###################################################################"
echo "* Installation finished. To continue, please edit your configuration file in"
echo "* /home/slave-nafsdm/config.conf aswell as copy over your SSH keys from the master."
echo ""
echo "* Thank you for using nafsdm!"
echo "###################################################################"
