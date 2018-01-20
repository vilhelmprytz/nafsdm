#!/bin/bash

cd /home/master-nafsdm/webinterface
/usr/bin/env gunicorn --workers=5 nafsdm_web:app
