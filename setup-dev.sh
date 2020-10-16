#!/bin/bash

#get current directory
current_working_dir=$(pwd)
#install python and venv
apt-get install python3 python3-venv python3.7-dev gcc
#create and activate environment
python3 -m venv app
cd app
chmod +x send
source ./bin/activate
#installe required python packages
pip3 install -r requirements.txt
export FLASK_ENV=development
python3 app.py