#!/bin/bash

#get latest version
git pull
#get current directory
current_working_dir=$(pwd)
#install python and venv
apt-get install python3 python3-venv
#create and activate environment
python3 -m venv app
cd app
source ./bin/activate
#installe required python packages
pip3 install -r requirements.txt
cd ..
#stop service in case its allready installed
systemctl stop a_pi_api
#create .service file
sed "s|__APP_DIR__|$current_working_dir|g" <a_pi_api.template.service >a_pi_api.service
mv a_pi_api.service /etc/systemd/system/a_pi_api.service
#lets go
systemctl daemon-reload
systemctl start a_pi_api
systemctl status a_pi_api
echo "use systemctl to controll the service"
echo "you can reach the api at http://%RASPBERRY_IP_ADDRESS:8000"