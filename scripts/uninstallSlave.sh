#!/bin/bash
# nafsdm
# uninstall script for nafsdm-slave
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

echo "* Are you sure you want to uninstall nafsdm-slave from this server?"
echo "* Please note: this uninstaller will NOT remove any Python libraries installed"
echo -n "* Confirm (y/n): "
read CONFIRM

if [ "$CONFIRM" == "y" ]; then
  echo "* Uninstalling .."

  /bin/systemctl stop nafsdm-slave.service

  rm -rf /home/slave-nafsdm
  rm -rf /usr/bin/nafscli
  rm -rf /etc/systemd/system/nafsdm-slave.service
  userdel slave-nafsdm

  echo "* Uninstalled!"
else
  echo "* Aborting.."
  exit 1
fi
