# nafsdm
# upgrade script for nafsdm slave
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

echo "* Welcome to nafsdm slave upgrade script!"

if [ "$OPERATINGSYS" == "centos" ]; then
  yum install curl wget -y
elif [[ "$OPERATINGSYS" == "debian" ]] || [[ "$OPERATINGSYS" == "ubuntu" ]] ; then
  apt-get install curl wget -y
else
  echo "* Invalid OS. Quit."
  exit 1
fi

OPERATINGSYS="$1"
BRANCH="$2"
DEV_IC_MODE="$3"
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
elif [ "$MY_VERSION_RAW" == 'version = "1.2.4-stable"' ]; then
  echo "* Detected version 1.2.4-stable - supported by this upgrade script."
  MY_VERSION="1.2.4-stable"
else
  echo "* Your version is not supported (dev versions and 1.0 is not supported)."
  exit 128
fi

echo "* Downloading newest version."
cd /tmp
if [ "$DEV_IC_MODE" == "True" ];
  git clone -b development https://github.com/MrKaKisen/nafsdm.git
else
  wget $DL_URL$LATEST_VERSION.tar.gz -O nafsdm.tar.gz
  tar -zxvf nafsdm.tar.gz
  mv nafsdm-* nafsdm
  rm -rf nafsdm.tar.gz
fi

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

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  echo "* Upgrade completed."
  echo "* Script has automatically modified your config to match with the new standards."

  exit 0

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

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

  exit 0

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

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

  exit 0

elif [ "$MY_VERSION" == "1.2.1-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # 1.2.2 > forward (replace start)
  rm -rf /home/slave-nafsdm/start.py
  cp nafsdm/slave-nafsdm/start.py /home/slave-nafsdm/start.py -R
  chmod +x /home/slave-nafsdm/start.py

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

  exit 0

elif [ "$MY_VERSION" == "1.2.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

  exit 0

elif [ "$MY_VERSION" == "1.2.3-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

  exit 0

elif [ "$MY_VERSION" == "1.2.4-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

  exit 0

elif [ "$MY_VERSION" == "1.2.5-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # nafscli reinstall (delete and copy) (from version 1.2.5 onwards)
  rm -rf /home/slave-nafsdm/nafscli
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

  exit 0

else
  echo "* Oops - something that shouldn't happen, happend anyways."
  exit 1
fi

# dev set version
if [ "$DEV_IC_MODE" == "y" ]; then
  cd /tmp/nafsdm
  COMMIT_HASH=$(git log -n 1 development | sed -n '1p' | cut -c8-14)
  echo "version = \"$COMMIT_HASH-dev\"" > /home/slave-nafsdm/pythondaemon/version.py
fi

rm -rf /tmp/nafsdm
