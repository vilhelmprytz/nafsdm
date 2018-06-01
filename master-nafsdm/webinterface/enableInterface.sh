#!/bin/bash

echo "* Would you like to enable the experimental nafsdm webinterface (not to use in a production environment)?"
echo -n "* Confirm (y/n): "
read CONFIRM

if [ "$CONFIRM" == "y" ]; then
  cp /home/master-nafsdm/webinterface/nafsdm-webinterface.service /etc/systemd/system/nafsdm-webinterface.service
  /usr/bin/env systemctl enable nafsdm-webinterface

  echo "* Enabled!"
  echo "* Please read the README.md before using."
  echo "* Start the webinterface with 'nafsdmctl webinterface start'."
else
  echo "* Aborting.."
  exit 1
fi
