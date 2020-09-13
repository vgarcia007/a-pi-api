import psutil
import os

from flask import Flask
from flask import jsonify

app = Flask(__name__)
#app.debug = True # Uncomment to debug

@app.route('/')
def home():
    return 'System Stats!'

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
        'load': str(psutil.cpu_percent()),
        'load_avg': str(psutil.getloadavg()),
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
        'total': str(total),
        'free': str(available),
        'free%': str(memory.percent)
        }
    return jsonify(response)


@app.route('/disk')
def disk():
    disk = psutil.disk_usage('/')
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free/1024.0/1024.0/1024.0,1)
    total = round(disk.total/1024.0/1024.0/1024.0,1)

    response = {
        'total': str(total),
        'free': str(free),
        'free%': str(disk.percent)
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')