#!/bin/bash

echo "* Would you like to enable the experimental nafsdm webinterface (not to use in a production environment)?"
echo -n "* Confirm (y/n): "
read CONFIRM

if [ "$CONFIRM" == "y" ]; then
  
else
  echo "* Aborting.."
  exit 1
fi
