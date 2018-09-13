#!/bin/bash

cd /opt/applications/job-monitor
[ -f env/bin/activate ] && source env/bin/activate && env/bin/python app.py || exit 1
