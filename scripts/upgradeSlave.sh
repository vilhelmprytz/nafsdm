# nafsdm
# upgrade script for nafsdm slave
# (c) Vilhelm Prytz 2017

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
  echo "* Invalid OS. Quit."
  exit 1
fi

BRANCH="master"
DL_URL="https://github.com/MrKaKisen/nafsdm/archive/"
MY_VERSION_RAW="`cat /home/slave-nafsdm/pythondaemon/version.py`"
LATEST_VERSION=$(curl https://raw.githubusercontent.com/MrKaKisen/nafsdm/$BRANCH/version.txt)

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

# perform upgrade
if [ "$MY_VERSION" == "1.0.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # this might be needed in the future,  but the script can currently fix itself :)
  #mv /home/slave-nafsdm/config.conf /home/slave-nafsdm/config-legacy.conf
  #cp nafsdm/slave-nafsdm/config.conf /home/slave-nafsdm/config.conf

  awk 'NR==1 {$0="[nafsdm]"} 1' /home/slave-nafsdm/config.conf > /home/slave-nafsdm/config.conf.temp
  rm -rf /home/slave-nafsdm/config.conf
  mv /home/slave-nafsdm/config.conf.temp /home/slave-nafsdm/config.conf

  # 1.2 > forward (enable on boot file)
  rm -rf /etc/systemd/system/nafsdm-slave.service
  cp nafsdm/systemconfigs/nafsdm-slave.service /etc/systemd/system/nafsdm-slave.service
  /usr/bin/env systemctl enable nafsdm-slave

  # 1.2.2 > forward (replace start)
  rm -rf /home/slave-nafsdm/start.py
  cp nafsdm/slave-nafsdm/start.py /home/slave-nafsdm/start.py -R
  chmod +x /home/slave-nafsdm/start.py

  # add nafscli shortcut (released in version 1.2.5)
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafsdmctl

  echo "* Upgrade completed."
  echo "* Script has automatically modified your config to match with the new standards."
elif [ "$MY_VERSION" == "1.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # 1.2 > forward (enable on boot file)
  rm -rf /etc/systemd/system/nafsdm-slave.service
  cp nafsdm/systemconfigs/nafsdm-slave.service /etc/systemd/system/nafsdm-slave.service
  /usr/bin/env systemctl enable nafsdm-slave

  # 1.2.2 > forward (replace start)
  rm -rf /home/slave-nafsdm/start.py
  cp nafsdm/slave-nafsdm/start.py /home/slave-nafsdm/start.py -R
  chmod +x /home/slave-nafsdm/start.py

  # add nafscli shortcut (released in version 1.2.5)
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafsdmctl

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh
elif [ "$MY_VERSION" == "1.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # 1.2 > forward (enable on boot file)
  rm -rf /etc/systemd/system/nafsdm-slave.service
  cp nafsdm/systemconfigs/nafsdm-slave.service /etc/systemd/system/nafsdm-slave.service
  /usr/bin/env systemctl enable nafsdm-slave

  # 1.2.2 > forward (replace start)
  rm -rf /home/slave-nafsdm/start.py
  cp nafsdm/slave-nafsdm/start.py /home/slave-nafsdm/start.py -R
  chmod +x /home/slave-nafsdm/start.py

  # add nafscli shortcut (released in version 1.2.5)
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafsdmctl

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh
elif [ "$MY_VERSION" == "1.2.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # 1.2.2 > forward (replace start)
  rm -rf /home/slave-nafsdm/start.py
  cp nafsdm/slave-nafsdm/start.py /home/slave-nafsdm/start.py -R
  chmod +x /home/slave-nafsdm/start.py

  # add nafscli shortcut (released in version 1.2.5)
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafsdmctl

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

elif [ "$MY_VERSION" == "1.2.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli shortcut (released in version 1.2.5)
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafsdmctl

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

elif [ "$MY_VERSION" == "1.2.3-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli shortcut (released in version 1.2.5)
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafsdmctl

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

elif [ "$MY_VERSION" == "1.2.4-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli shortcut (released in version 1.2.5)
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafsdmctl

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

else
  echo "* Oops - something that shouldn't happen, happend anyways."
  exit 1
fi

rm -rf /tmp/nafsdm
