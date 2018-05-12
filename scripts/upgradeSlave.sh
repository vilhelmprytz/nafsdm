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

# set OPERATINGSYS first
OPERATINGSYS="$1"

if [ "$OPERATINGSYS" == "centos" ]; then
  yum install curl wget git -y
elif [[ "$OPERATINGSYS" == "debian" ]] || [[ "$OPERATINGSYS" == "ubuntu" ]] ; then
  apt-get install curl wget git -y
else
  echo "* Invalid OS. Quit."
  exit 1
fi

BRANCH="$2"
DEV_IC_MODE="$3"
DL_URL="https://github.com/MrKaKisen/nafsdm/archive/"
MY_VERSION_RAW="`cat /home/slave-nafsdm/pythondaemon/version.py`"
LATEST_VERSION=$(curl https://raw.githubusercontent.com/MrKaKisen/nafsdm/$BRANCH/version.txt)
REQ_URL="https://raw.githubusercontent.com/MrKaKisen/nafsdm/$BRANCH/scripts/requirements_slave.txt"

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
else
  if [ "$DEV_IC_MODE" == "False" ]; then
    echo "* Your version is not supported (dev versions and 1.0 is not supported)."
    exit 128
  else
    MY_VERSION="dev_release"
  fi
fi

echo "* Downloading newest version."
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

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

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

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

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

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

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

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

elif [ "$MY_VERSION" == "1.2.2-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

elif [ "$MY_VERSION" == "1.2.3-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

elif [ "$MY_VERSION" == "1.2.4-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # add nafscli (released in version 1.2.5)
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R
  cp nafsdm/systemconfigs/nafscli /usr/bin/nafscli
  chmod +x /usr/bin/nafscli

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

elif [ "$MY_VERSION" == "1.2.5-stable" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # nafscli reinstall (delete and copy) (from version 1.2.5 onwards)
  rm -rf /home/slave-nafsdm/nafscli
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R

  # add new development section to config file (versions after 1.2.5) & added new options section
  echo -e "\n[options]\nupgradeOnStart = False" >> /home/slave-nafsdm/config.conf
  echo -e "\n[development]\ngithub_branch = master\nskipVersionCheck = False\nincrementalCommitVersions = False" >> /home/slave-nafsdm/config.conf

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

# for dev versions
elif [ "$MY_VERSION" == "dev_release" ]; then
  echo "* Replacing python files.."
  rm -rf /home/slave-nafsdm/pythondaemon
  cp nafsdm/slave-nafsdm/pythondaemon /home/slave-nafsdm/pythondaemon -R

  # nafscli reinstall (delete and copy) (from version 1.2.5 onwards)
  rm -rf /home/slave-nafsdm/nafscli
  cp nafsdm/slave-nafsdm/nafscli /home/slave-nafsdm/nafscli -R

  # dev set version
  if [ "$DEV_IC_MODE" == "True" ]; then
    echo "* Setting dev version.."

    cd /tmp/nafsdm
    COMMIT_HASH=$(git log -n 1 development | sed -n '1p' | cut -c8-14)
    echo "version = \"$COMMIT_HASH-dev\"" > /home/slave-nafsdm/pythondaemon/version.py

    echo "* Done."
  fi

  # install from req file (released in version 1.3.1)
  pip install -r requirements.txt
  rm -rf requirements.txt

  echo "* Upgrade completed. You can now start nafsdm-slave again (make sure master is also upgraded!)-"
  echo "* Make sure to copy the [development] section into config.conf and make sure branch is set to development and that incrementalCommitVersions is set to True."
  rm -rf /home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh

else
  echo "* Oops - something that shouldn't happen, happend anyways."
  exit 1
fi

rm -rf /tmp/nafsdm
exit 0
