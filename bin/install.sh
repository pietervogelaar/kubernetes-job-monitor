#!/bin/bash

[ -d /opt/applications/job-monitor ] || exit 1
cd /opt/applications/job-monitor
virtualenv --no-site-packages env
source env/bin/activate
pip install -r requirements.txt
sudo systemctl restart job-monitor
