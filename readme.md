# a pi api

Flask app served by gunicorn that provides raspberry system information as json.

After installation this runs as a service and is reachable at Port 8000.

Tested with Stretch and Buster Raspberry OS.

## Routes

*URL: http://raspberry:8000/*

```json
{
  "distribution": "debian",
  "distribution_verson": "9.13",
  "hostname": "raspberrypi",
  "mac_address": "b8:27:eb:d9:9f:f2"
}
```

*URL: http://raspberry:8000/cpu*

```json
{
  "freq": 600,
  "load": 1.1,
  "load_avg": [
    0.0,
    0.0,
    0.0
  ],
  "temp": 59
}
```

*URL: http://raspberry:8000/memory*

```json
{
  "free": 614.8,
  "free_perc": 33.6,
  "total": 926.1
}
```

*URL: http://raspberry:8000/disk*

```json
{
  "free": "11.4",
  "free%": "18.4",
  "total": "14.6"
}
```

## Installation

```bash
git clone https://github.com/vgarcia007/a-pi-api.git
cd a-pi-api
sudo /bin/bash setup.sh
```

## Service start/status/stop

```bash
systemctl start a_pi_api
systemctl status a_pi_api
systemctl stop a_pi_api
```

## Remove service
```bash
sudo rm /etc/systemd/system/a_pi_api.service
sudo systemctl daemon-reload
```

## Start test server without installing a service

```bash
apt-get install python3 python3-venv
python3 -m venv app
cd app
source ./bin/activate
pip3 install -r requirements.txt
/bin/bash dev-server.sh
```

## ToDo

Add Routes for sensors attached to GPIO like 1-Wire

## License
[WTFPL](https://choosealicense.com/licenses/wtfpl/)
