# nafsdm
# upgrade script for nafsdm master
# (c) Vilhelm Prytz 2017

# check if user is root or not
if [[ $EUID -ne 0 ]]; then
  echo "* This script must be run with root privileges (sudo)." 1>&2
  exit 1
fi

echo "* Welcome to nafsdm master upgrade script!"

# as nafsdm-master doesn't know if it's centos or debian, this command should generally work.
python -mplatform | grep -qi Ubuntu && echo "debian" > /home/master-nafsdm/system-type.txt || echo "centos" > /home/master-nafsdm/system-type.txt
python -mplatform | grep -qi debian && echo "debian" > /home/master-nafsdm/system-type.txt || echo "centos" > /home/master-nafsdm/system-type.txt

OPERATINGSYS="`cat /home/master-nafsdm/system-type.txt`"

if [ "$OPERATINGSYS" == "centos" ]; then
  yum install curl wget -y
elif [[ "$OPERATINGSYS" == "debian" ]] || [[ "$OPERATINGSYS" == "ubuntu" ]] ; then
  apt-get install curl wget -y
else
  echo "* Invalid OS. Quit."
  exit 1
fi

BRANCH="master"
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
else
  echo "* Your version is not supported (dev versions and 1.0 is not supported)."
  exit 1
fi

echo "* Downloading newest version."
cd /tmp
wget $DL_URL$LATEST_VERSION.tar.gz -O nafsdm.tar.gz
tar -zxvf nafsdm.tar.gz
mv nafsdm-* nafsdm
rm -rf nafsdm.tar.gz

# req dl
wget -O requirements.txt $REQ_URL

# perform upgrade
if [ "$MY_VERSION" == "1.0.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.3
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsm/webinterface/nafsdm-webinterface.service

  # newer than version 1.3
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. Note: before you start all slaves, update the /home/master-nafsdm/data/domains.txt to use the new DNSSEC support!"
  echo "* After the list of slaves in the config, add a space and this: 'dnssec.yes' (without colons). Replace yes with no if the domain does not use dnssec."
  echo "* NAFSDM WILL NOT START IF THIS SCRIPT EXISTS. DELETE IT BEFORE START."
elif [ "$MY_VERSION" == "1.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.3
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsm/webinterface/nafsdm-webinterface.service

  # newer than version 1.3
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. Note: before you start all slaves, update the /home/master-nafsdm/data/domains.txt to use the new DNSSEC support!"
  echo "* After the list of slaves in the config, add a space and this: 'dnssec.yes' (without colons). Replace yes with no if the domain does not use dnssec."
  echo "* NAFSDM WILL NOT START IF THIS SCRIPT EXISTS. DELETE IT BEFORE START."
elif [ "$MY_VERSION" == "1.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.3
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsm/webinterface/nafsdm-webinterface.service

  # newer than version 1.3
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Update completed. Nothing to do or change!"
elif [ "$MY_VERSION" == "1.2.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.3
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsm/webinterface/nafsdm-webinterface.service

  # newer than version 1.3
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Update completed. Nothing to do or change!"
elif [ "$MY_VERSION" == "1.2.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.3
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsm/webinterface/nafsdm-webinterface.service

  # newer than version 1.3
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Update completed. Nothing to do or change!"
elif [ "$MY_VERSION" == "1.2.3-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/master-nafsdm/pythondaemon
  rm -rf /home/master-nafsdm/nafsdmctl
  cp nafsdm/master-nafsdm/pythondaemon /home/master-nafsdm/pythondaemon -R
  cp nafsdm/master-nafsdm/nafsdmctl /home/master-nafsdm/nafsdmctl -R

  # newer than version 1.3
  cp nafsdm/master-nafsdm/webinterface /home/master-nafsdm/webinterface -R
  cp nafsdm/systemconfigs/nafsdm-webinterface.service /home/master-nafsm/webinterface/nafsdm-webinterface.service

  # newer than version 1.3
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Update completed. Nothing to do or change!"
else
  echo "* Oops - something that shouldn't happen, happend anyways."
  exit 1
fi

rm -rf /tmp/nafsdm
