# a pi api

Flask app served by gunicorn that provides raspberry system information as json.

After installation this runs as a service and is reachable at Port 8000.

Tested with Stretch and Buster Raspberry OS.

## Routes

*URL: http<nolink>://raspberry:8000/*

```json
{
  "api_Version": "bc39db2",
  "distribution": "debian",
  "distribution_verson": "9.13",
  "hostname": "raspberrypi",
  "mac_address": "b8:27:eb:d9:9f:f2"
}
```

If 1-wire ds1820 sensors are present they will be listed
```json
{
  "api_Version": "234c33c",
  "distribution": "debian",
  "distribution_verson": "9.13",
  "hostname": "RPIserverschrank",
  "mac_address": "b8:27:eb:d9:9f:f2",
  "one_wire": {
    "ds1820": [
      "28-02183316b6ff",
      "28-0218335796ff"
      ]
    }
}
```

*URL: http<nolink>://raspberry:8000/one-wire/ds1820/sensor*  
**Example**  
http<nolink>://raspberry:8000/one-wire/ds1820/28-02183316b6ff
```json
{
  "temp_c": 26.25,
  "temp_f": 79.25
}
```

*URL: http<nolink>://raspberry:8000/cpu*
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

*URL: http<nolink>://raspberry:8000/memory*
```json
{
  "free": 614.8,
  "free_perc": 33.6,
  "total": 926.1
}
```

*URL: http<nolink>://raspberry:8000/disk*
```json
{
  "free": 11.4,
  "free%": 18.4,
  "total": 14.6
}
```
### Control 433 switches

*URL: http<nolink>://raspberry:8000/send433mhz/housecode/devicecode/state*
```json
{
"stderr": "b''",
"stdout": "b'using pin 0\\nsending systemCode[00011] unitCode[2] command[0]\\n'"
}
```
**Example**  
http<nolink>://raspberry:8000/send433mhz/00011/2/0 (off)  
http<nolink>://raspberry:8000/send433mhz/00011/2/1 (on)

**Credits**  
For this to work a-pi-api ships with a compiled version of "raspberry-remote" (https://github.com/xkonni/raspberry-remote)


## Installation

```bash
git clone https://github.com/vgarcia007/a-pi-api.git
cd a-pi-api
sudo /bin/bash update.sh
```
This way, the api and its dependencies are installed.

In addition, a system service is created in "/etc/systemd/system/". So that after a restart of the Raspberry the server starts again.

After successful execution, the http server is available on port 8000.

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
The test http server is available on port 5000.

## ToDo

* Add routes for more sensor types attached to GPIO
* Add Moduls for other things like nas and fritzbox

## License
[WTFPL](https://choosealicense.com/licenses/wtfpl/)
