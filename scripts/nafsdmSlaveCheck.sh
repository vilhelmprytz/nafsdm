#!/bin/bash
# nafsdm
# extra script: checks if the nafsdm slave is running or not
# (c) Vilhelm Prytz 2018

GREP_FAILED=$(/bin/systemctl status nafsdm-slave.service | grep "Active: failed")
GREP_INACTIVE=$(/bin/systemctl status nafsdm-slave.service | grep "Active: inactive")

if [ "$GREP_FAILED" == "" ]; then
  STATUS="running"
else
  echo "nafsdm slave is marked as failed. Output: "
  echo "$GREP_FAILED"
  exit 2
fi

if [ "$GREP_INACTIVE" == "" ]; then
  STATUS="running"
else
  echo "nafsdm slave is marked as inactive. Output: "
  echo "$GREP_INACTIVE"
  exit 2
fi

echo "status: $STATUS"
exit 0
