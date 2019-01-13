#!/bin/bash

# Start supervisor
exec /usr/bin/supervisord -n -c /etc/supervisord.conf
