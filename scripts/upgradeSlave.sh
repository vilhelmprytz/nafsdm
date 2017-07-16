# nafsdm
# upgrade script for nafsdm slave
# Copyright Vilhelm Prytz 2017

# check if user is root or not
if [[ $EUID -ne 0 ]]; then
  echo "* This script must be run with root privileges (sudo)." 1>&2
  exit 1
fi

echo "* Welcome to nafsdm slave upgrade script!"

echo -n "* Enter operating system (debian/ubuntu/centos): "
OPERATINGSYS="$1"

if [ "$OPERATINGSYS" == "centos" ]; then
  yum install curl wget -y
elif [[ "$OPERATINGSYS" == "debian" ]] || [[ "$OPERATINGSYS" == "ubuntu" ]] ; then
  apt-get install curl wget -y
else

fi

DL_URL="https://github.com/MrKaKisen/nafsdm/archive/"
MY_VERSION_RAW="`cat /home/master-nafsdm/pythondaemon/version.py`"
LATEST_VERSION=$(curl https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/version.txt)

# determine supported versions
if [ "$MY_VERSION_RAW" == 'version = "1.0.1-stable"' ]; then
  echo "* Detected version 1.0.1-stable - supported by this upgrade script."
  MY_VERSION="1.0.1-stable"
elif [ "$MY_VERSION_RAW" == 'version = "1.1-stable"' ]; then
  echo "* Detected version 1.1-stable - supported by this upgrade script."
  MY_VERSION="1.1-stable"
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

# perform upgrade
if [ "$MY_VERSION" == "1.0.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  mv /home/slave-nafsdm/config.conf /home/slave-nafsdm/config-legacy.conf
  cp nafsdm/slave-nafsdm/config.conf /home/slave-nafsdm/config.conf

  echo "* Upgrade completed."
  echo "* Before you start, re-enter your configuration in /home/slave-nafsdm/config.conf as that has changed in version 1.2."
  echo "* Your old config is also saved as /home/slave-nafsdm/config-legacy.conf"
  echo "* NAFSDM WILL NOT START IF THIS SCRIPT EXISTS. DELETE IT BEFORE START."
elif [ "$MY_VERSION" == "1.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh
else
  echo "* Oops - something that shouldn't happen, happend anyways."
  exit 1
