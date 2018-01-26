#!/bin/bash

cd /home/master-nafsdm/webinterface
/usr/bin/env gunicorn --workers=5 --bind 0.0.0.0:8000 nafsdm_web:app
