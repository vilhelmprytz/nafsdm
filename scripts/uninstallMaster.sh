#!/bin/bash
# nafsdm
# uninstall script for nafsdm-master
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

echo "* Are you sure you want to uninstall nafsdm-master from this server?"
echo "* Please note: this uninstaller will NOT remove any Python libraries installed"
echo -n "* Confirm (y/n): "
read CONFIRM

if [ "$CONFIRM" == "y" ]; then
  echo "* Uninstalling .."

  rm -rf /home/master-nafsdm
  rm -rf /usr/bin/nafsdmctl
  rm -rf /usr/bin/nafsdm-master
  # as of version 1.4-stable, nafsdm-master is renamed to nafsdm-manager
  rm -rf /usr/bin/nafsdm-manager
  userdel master-nafsdm

  rm -rf /etc/systemd/system/nafsdm-webinterface.service
  rm -rf /etc/systemd/system/nafsdm-daemon.service

  echo "* Uninstalled!"
else
  echo "* Aborting.."
  exit 1
fi
