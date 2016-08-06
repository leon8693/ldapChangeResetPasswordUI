#!/bin/bash
set -e
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi
apt-get install python-pip python-dev  -y
apt-get install python-dev libldap2-dev libsasl2-dev libssl-dev libmysqlclient-dev -y
pip install -r requirements.txt
