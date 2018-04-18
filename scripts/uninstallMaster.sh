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
  userdel master-nafsdm

  rm -rf /home/master-nafsdm/webinterface/nafsdm-webinterface.service

  echo "* Uninstalled!"
else
  echo "* Aborting.."
  exit 1
fi
