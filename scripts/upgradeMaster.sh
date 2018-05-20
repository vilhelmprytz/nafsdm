# nafsdm
# upgrade script for nafsdm master
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# Exit codes:
# normal - 0
# error - 1
# unsupported version - 128

# check if user is root or not
if [[ $EUID -ne 0 ]]; then
  echo "* This script must be run with root privileges (sudo)." 1>&2
  exit 1
fi

DATE="`date`"

echo "###################################################################"
echo "* nafsdm-master upgrade script script"
echo "* date: $DATE"
echo "###################################################################"

# as nafsdm-master doesn't know if it's centos or debian, this command should generally work.
python -mplatform | grep -qi Ubuntu && echo "debian" > /home/master-nafsdm/system-type.txt || echo "centos" > /home/master-nafsdm/system-type.txt
python -mplatform | grep -qi debian && echo "debian" > /home/master-nafsdm/system-type.txt || echo "centos" > /home/master-nafsdm/system-type.txt

OPERATINGSYS="`cat /home/master-nafsdm/system-type.txt`"

if [ "$OPERATINGSYS" == "centos" ]; then
  echo "* Installing required packages for CentOS.."
  yum install curl wget git -y
elif [[ "$OPERATINGSYS" == "debian" ]] || [[ "$OPERATINGSYS" == "ubuntu" ]] ; then
  echo "* Installing required packages for Debian/Ubuntu.."
  apt-get install curl wget git -y
else
  echo "* Invalid OS. Quit."
  exit 1
fi

BRANCH="$1"
DEV_IC_MODE="$2"
DL_URL="https://github.com/MrKaKisen/nafsdm/archive/"
MY_VERSION_RAW="`cat /home/master-nafsdm/pythondaemon/version.py`"
LATEST_VERSION=$(curl https://raw.githubusercontent.com/MrKaKisen/nafsdm/$BRANCH/version.txt)
REQ_URL="https://raw.githubusercontent.com/MrKaKisen/nafsdm/$BRANCH/scripts/requirements_master.txt"

# determine supported versions
if [ "$MY_VERSION_RAW" == 'version = "1.0.1-stable"' ]; then
  echo "* Detected version 1.0.1-stable - supported by this upgrade script."
  MY_VERSION="1.0.1-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.1-stable"' ]; then
  echo "* Detected version 1.1-stable - supported by this upgrade script."
  MY_VERSION="1.1-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.2-stable"' ]; then
  echo "* Detected version 1.2-stable - supported by this upgrade script."
  MY_VERSION="1.2-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.2.1-stable"' ]; then
  echo "* Detected version 1.2.1-stable - supported by this upgrade script."
  MY_VERSION="1.2.1-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.2.2-stable"' ]; then
  echo "* Detected version 1.2.2-stable - supported by this upgrade script."
  MY_VERSION="1.2.2-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.2.3-stable"' ]; then
  echo "* Detected version 1.2.3-stable - supported by this upgrade script."
  MY_VERSION="1.2.3-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.2.4-stable"' ]; then
  echo "* Detected version 1.2.4-stable - supported by this upgrade script."
  MY_VERSION="1.2.4-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.2.5-stable"' ]; then
  echo "* Detected version 1.2.5-stable - supported by this upgrade script."
  MY_VERSION="1.2.5-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.3-stable"' ]; then
  echo "* Detected version 1.3-stable - supported by this upgrade script."
  MY_VERSION="1.3-stable"
else
  if [ "$DEV_IC_MODE" == "False" ]; then
    echo "* Your version is not supported (dev versions and 1.0 is not supported)."
    exit 128
  else
    echo "* Detected dev_release (commit update mode)."
    MY_VERSION="dev_release"
  fi
fi

echo "* Downloading newest release."
cd /tmp
if [ "$DEV_IC_MODE" == "True" ]; then
  git clone -b development https://github.com/MrKaKisen/nafsdm.git
else
  wget $DL_URL$LATEST_VERSION.tar.gz -O nafsdm.tar.gz
  tar -zxvf nafsdm.tar.gz
  mv nafsdm-* nafsdm
  rm -rf nafsdm.tar.gz
fi

# req dl
wget -O requirements.txt $REQ_URL

# as of version 1.3.1, we also copy the CHANGELOG
rm -rf /home/master-nafsdm/changelog.txt
cp /tmp/nafsdm/CHANGELOG.md /home/master-nafsdm/changelog.txt

# perform upgrade
if [ "$MY_VERSION" == "1.0.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4
  echo "* Installing webinterface.."
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Upgrade completed. Note: before you start all slaves, update the /home/master-nafsdm/data/domains.txt to use the new DNSSEC support!"
  echo "* After the list of slaves in the config, add a space and this: 'dnssec.yes' (without colons). Replace yes with no if the domain does not use dnssec."
  echo "* NAFSDM WILL NOT START IF THIS SCRIPT EXISTS. DELETE IT BEFORE START."

elif [ "$MY_VERSION" == "1.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4
  echo "* Installing webinterface.."
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Upgrade completed. Note: before you start all slaves, update the /home/master-nafsdm/data/domains.txt to use the new DNSSEC support!"
  echo "* After the list of slaves in the config, add a space and this: 'dnssec.yes' (without colons). Replace yes with no if the domain does not use dnssec."
  echo "* NAFSDM WILL NOT START IF THIS SCRIPT EXISTS. DELETE IT BEFORE START."

elif [ "$MY_VERSION" == "1.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4
  echo "* Installing webinterface.."
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Update completed. Nothing to do or change!"

elif [ "$MY_VERSION" == "1.2.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4
  echo "* Installing webinterface.."
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Update completed. Nothing to do or change!"

elif [ "$MY_VERSION" == "1.2.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4
  echo "* Installing webinterface.."
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Update completed. Nothing to do or change!"

elif [ "$MY_VERSION" == "1.2.3-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4
  echo "* Installing webinterface.."
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Update completed. Nothing to do or change!"

elif [ "$MY_VERSION" == "1.2.4-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4, all versions that already have the webinterface
  echo "* Replacing webinterface.."

  # save password
  cp /home/master-nafsdm/interfacePassword.txt /tmp/interfacePassword.txt

  rm -rf /home/master-nafsdm/webinterface
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # add back password
  rm -rf /home/master-nafsdm/interfacePassword.txt
  cp /tmp/interfacePassword.txt /home/master-nafsdm/interfacePassword.txt
  # webinterface done

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Update completed. Nothing to do or change!"

elif [ "$MY_VERSION" == "1.2.5-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4, all versions that already have the webinterface
  echo "* Replacing webinterface.."

  # save password
  cp /home/master-nafsdm/interfacePassword.txt /tmp/interfacePassword.txt

  rm -rf /home/master-nafsdm/webinterface
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # add back password
  rm -rf /home/master-nafsdm/interfacePassword.txt
  cp /tmp/interfacePassword.txt /home/master-nafsdm/interfacePassword.txt
  # webinterface done

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Update completed. Nothing to do or change!"

elif [ "$MY_VERSION" == "1.3-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4, all versions that already have the webinterface
  echo "* Replacing webinterface.."

  # save password
  cp /home/master-nafsdm/interfacePassword.txt /tmp/interfacePassword.txt

  rm -rf /home/master-nafsdm/webinterface
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # add back password
  rm -rf /home/master-nafsdm/interfacePassword.txt
  cp /tmp/interfacePassword.txt /home/master-nafsdm/interfacePassword.txt
  # webinterface done

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  echo "* Update completed. Nothing to do or change!"

# for dev versions
elif [ "$MY_VERSION" == "dev_release" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.2.4, all versions that already have the webinterface
  echo "* Replacing webinterface.."

  # save password
  cp /home/master-nafsdm/interfacePassword.txt /tmp/interfacePassword.txt

  rm -rf /home/master-nafsdm/webinterface
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsdm/webinterface/nafsdm-webinterface.service
  chmod +x /home/master-nafsdm/webinterface/enableInterface.sh
  chmod +x /home/master-nafsdm/webinterface/start.sh

  # add back password
  rm -rf /home/master-nafsdm/interfacePassword.txt
  cp /tmp/interfacePassword.txt /home/master-nafsdm/interfacePassword.txt
  # webinterface done

  # newer than version 1.2.4
  echo "* Installing required python packages.."
  pip install -r requirements.txt
  rm -rf requirements.txt

  # from version 1.3 onwards
  if [ ! -d "/home/master-nafsdm/slaveAlive" ]; then
    mkdir /home/master-nafsdm/slaveAlive
  fi
  chown -R master-nafsdm:master-nafsdm /home/master-nafsdm/slaveAlive

  # dev set version
  if [ "$DEV_IC_MODE" == "True" ]; then
    echo "* Setting dev version.."

    cd /tmp/nafsdm
    COMMIT_HASH=$(git log -n 1 development | sed -n '1p' | cut -c8-14)
    echo "version = \"$COMMIT_HASH-dev\"" > /home/master-nafsdm/pythondaemon/version.py
    echo "True" > /home/master-nafsdm/pythondaemon/dev_ic_mode.txt
    echo "development" > /home/master-nafsdm/pythondaemon/dev_github_branch.txt

    echo "* Done."
  fi

  echo "* Update completed. Nothing to do or change!"

else
  echo "* Oops - something that shouldn't happen, happend anyways."
  exit 1
fi

DATE="`date`"
echo "* Finished @ $DATE"

rm -rf /tmp/nafsdm
exit 0
