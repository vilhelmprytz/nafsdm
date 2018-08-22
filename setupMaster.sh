# nafsdm
# help script for setting up nafsdm on the master
# Copyright Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# check if user is root or not
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run with root privileges (sudo)." 1>&2
  exit 1
fi

# check for python
PYTHONPATH="$(which python)"
if [ -z "$PYTHONPATH" ]; then
    echo "* Python is required in order for this script to work."
    echo "* install using apt on Debian/Ubuntu or yum on CentOS"
    exit 1
fi

# variables
CLONE_URL="https://github.com/MrKaKisen/nafsdm.git"
CLONE_BRANCH="development"
DL_URL="https://github.com/MrKaKisen/nafsdm/archive/"
REQ_URL="https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/scripts/requirements_master.txt"
GITHUB_DIR="master-nafsdm"
HOME_DIR="/home/master-nafsdm"
USER="master-nafsdm"

# visual functions
function print_error {
  COLOR_RED='\033[0;31m'
  COLOR_NC='\033[0m'

  echo ""
  echo -e "* ${COLOR_RED}ERROR${COLOR_NC}: $1"
  echo ""
}

# os detection
function detect_distro {
  echo "$(python -c 'import platform ; print platform.dist()[0]')" | awk '{print tolower($0)}'
}

function detect_os_version {
  echo "$(python -c 'import platform ; print platform.dist()[1].split(".")[0]')"
}

function check_os_comp {
  if [ "$OS" == "ubuntu" ]; then
    if [ "$OS_VERSION" == "16" ]; then
      SUPPORTED=true
    elif [ "$OS_VERSION" == "18" ]; then
      SUPPORTED=true
    else
      SUPPORTED=false
    fi
  elif [ "$OS" == "debian" ]; then
    if [ "$OS_VERSION" == "9" ]; then
      SUPPORTED=true
    else
      SUPPORTED=false
    fi
  elif [ "$OS" == "centos" ]; then
    if [ "$OS_VERSION" == "7" ]; then
      SUPPORTED=true
    else
      SUPPORTED=false
    fi
  else
    SUPPORTED=false
  fi

  # exit if not supported
  if [ "$SUPPORTED" == true ]; then
    echo "* $OS $OS_VERSION is supported."
  else
    echo "* $OS $OS_VERSION is not supported"
    print_error "Unsupported OS"
    exit 1
  fi
}

echo "###################################################################"
echo "* nafsdm-master installation script"
echo "* note: this installer will not upgrade your installation"
echo "###################################################################"
echo "* Detecting operating system."
OS=$(detect_distro);
OS_VERSION=$(detect_os_version);
echo "* Running $OS version $OS_VERSION."

echo "###################################################################"
# checks if the system is compatible
check_os_comp

if [ "$OS" == "centos" ]; then
  echo "* Installing packages.."
  yum update -y
  yum install python curl wget -y

  # centos does not have pip in it's repos
  curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
  python get-pip.py
  rm get-pip.py -rf

  cd /tmp
  wget -O requirements.txt $REQ_URL

  pip install -r requirements.txt
  rm -rf requirements.txt
elif [[ "$OS" == "debian" ]] || [[ "$OS" == "ubuntu" ]] ; then
  echo "* Installing packages.."
  apt-get update -y
  apt-get install python python-pip curl wget -y

  cd /tmp
  wget -O requirements.txt $REQ_URL

  pip install -r requirements.txt
  rm -rf requirements.txt
else
  print_error "Invalid operating system. Only 'debian', 'ubuntu' and 'centos' supported."
  exit 1
fi

# get which version is the latest
echo "* Fetching information about latest version.."
LATEST_VERSION=$(curl https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/version.txt)

# commit updates
echo "* Developers only: Would you like to enable incremental commit updates and use development branch only?"
echo "* Warning: This is a developer function, do not use in a production environment."
echo -n "* Enable? (y/n): "
read DEV_IC_CONFIRM

if [ "$DEV_IC_CONFIRM" == "y" ]; then
  if [ "$OS" == "centos" ]; then
    yum install git -y
  elif [[ "$OS" == "debian" ]] || [[ "$OS" == "ubuntu" ]] ; then
    apt-get install git -y
  else
    print_error "Invalid operating system."
    exit 1
  fi

  cd /tmp
  git clone -b $CLONE_BRANCH $CLONE_URL
elif [ "$DEV_IC_CONFIRM" == "n" ]; then
  echo "* Skipping.."
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
else
  echo "* Aborting.."
  exit 1
fi

echo "* Required packages installed!"
echo "* Downloading nafsdm & installing.."

# download in temp dir
if [ "$DEV_IC_CONFIRM" == "n" ]; then
  cd /tmp
  wget $DL_URL$DL_VERSION.tar.gz -O nafsdm.tar.gz
  tar -zxvf nafsdm.tar.gz
  mv nafsdm-* nafsdm
fi

cd /tmp

useradd $USER
# debian and ubuntu doesn't create its home dir automatically, unlike centos
if [[ "$OS" == "debian" ]] || [[ "$OS" == "ubuntu" ]] ; then
  mkdir $HOME_DIR
fi
mkdir $HOME_DIR/.ssh
mkdir $HOME_DIR/slaveAlive
chown -R master-nafsdm:master-nafsdm $HOME_DIR/.ssh
chown -R master-nafsdm:master-nafsdm $HOME_DIR/slaveAlive
cp /tmp/nafsdm/$GITHUB_DIR /home -R
cp /tmp/nafsdm/LICENSE $HOME_DIR/LICENSE

cp /tmp/nafsdm/systemconfigs/nafsdmctl /usr/bin/nafsdmctl
cp /tmp/nafsdm/systemconfigs/nafsdm-manager /usr/bin/nafsdm-manager

# nafsdm webinterface
cp /tmp/nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
chmod +x /home/master-nafsdm/webinterface/start.sh

# as of version 1.3.1, we also copy the CHANGELOG
cp /tmp/nafsdm/CHANGELOG.md $HOME_DIR/changelog.txt

chmod +x /usr/bin/nafsdmctl
chmod +x /usr/bin/nafsdm-manager
chmod +x /home/master-nafsdm/startDaemon.py

# enable systemd service
#cp /tmp/nafsdm/systemconfigs/nafsdm-daemon.service /etc/systemd/system/nafsdm-daemon.service
#/usr/bin/env systemctl enable nafsdm-daemon

# dev set version
if [ "$DEV_IC_CONFIRM" == "y" ]; then
  cd /tmp/nafsdm
  COMMIT_HASH=$(git log -n 1 development | sed -n '1p' | cut -c8-14)
  echo "version = \"$COMMIT_HASH-dev\"" > /home/master-nafsdm/manager/version.py
  echo "True" > /home/master-nafsdm/manager/dev_ic_mode.txt
  echo "development" > /home/master-nafsdm/manager/dev_github_branch.txt
fi

# and actually start the daemon
#/usrbin/env systemctl start nafsdm-daemon

echo "* Installed. Cleanup.."

rm /tmp/nafsdm -rf
echo "###################################################################"
echo "* nafsdm-master installation complete"
echo "* To continue, please run 'nafsdm-manager' for first time setup."
echo "* Thank you for using nafsdm!"
echo "###################################################################"
