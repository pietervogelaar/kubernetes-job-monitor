#!/bin/bash

# Make sure the kubeconfig file exists to avoid errors with kubectl
mkdir /etc/.kube
touch /etc/.kube/config

# Start supervisor
exec /usr/bin/supervisord -n -c /etc/supervisord.conf
