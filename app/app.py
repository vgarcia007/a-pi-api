import psutil
import os
import sys
import time
import platform
import socket
import re
import uuid
from version import version
from flask import Flask
from flask import jsonify


app = Flask(__name__)

@app.route('/')
def home():

    def list_ds1820():
        sensors =[]
        try:
            for sensor in os.listdir("/sys/bus/w1/devices"):
                if (sensor.split("-")[0] == "28") or (sensor.split("-")[0] == "10"):
                    sensors.append(sensor)
        except:
            pass

        return sensors

    distri = platform.dist()

    response = {
        'distribution': distri[0],
        'distribution_verson': distri[1],
        'hostname': str(socket.gethostname()),
        'mac_address': str(':'.join(re.findall('..', '%012x' % uuid.getnode()))),
        'api_Version': version,
        }

    one_wire = list_ds1820()
    if one_wire:
        response['one_wire'] = {}
        response['one_wire']['ds1820'] = one_wire

    return jsonify(response)

@app.route('/cpu')
def cpu():

    def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        res = res.replace("temp=", "")
        res = res.replace("'C", "")
        return res

    def getCPUfrequ():
        
        freq = str(psutil.cpu_freq())
        freq_list = freq.split(',')
        freq_current = freq_list[0].replace("scpufreq(current=", "")
        return freq_current

    response = {
        'load': psutil.cpu_percent(),
        'load_avg': psutil.getloadavg(),
        'freq': int(float(getCPUfrequ())),
        'temp': int(float(getCPUtemperature()))
        }
    return jsonify(response)


@app.route('/memory')
def memory():
    memory = psutil.virtual_memory()
    # Divide from Bytes -> KB -> MB
    available = round(memory.available/1024.0/1024.0,1)
    total = round(memory.total/1024.0/1024.0,1)
    response = {
        'total': total,
        'free': available,
        'free_perc': memory.percent
        }
    return jsonify(response)


@app.route('/disk')
def disk():
    disk = psutil.disk_usage('/')
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free/1024.0/1024.0/1024.0,1)
    total = round(disk.total/1024.0/1024.0/1024.0,1)

    response = {
        'total': total,
        'free': free,
        'free%': disk.percent
        }
    return jsonify(response)

@app.route('/one-wire/ds1820/<sensor>')
def read_ds1820(sensor):

    def read_temp_raw(sensor):
        try:
            f = open('/sys/bus/w1/devices/' + sensor + '/w1_slave', 'r')
            lines = f.readlines()
            f.close()
            return lines
        except:
            return 'error'

    def read_temp(sensor):
        temp = {}

        lines = read_temp_raw(sensor)
        if 'error' in lines:
            return 'error'
            
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp['temp_c'] = round((float(temp_string) / 1000.0), 2)
            temp['temp_f'] = round((temp['temp_c'] * 9.0 / 5.0 + 32.0), 2)
            return temp


    response = read_temp(sensor)

    return jsonify(response)



if __name__ == '__main__':
    app.run(host='0.0.0.0')