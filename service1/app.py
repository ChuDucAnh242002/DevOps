from flask import Flask, jsonify, render_template
import psutil
import socket
import requests
import time
import docker

app = Flask(__name__)

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return ip_address

def get_running_processes():
    processes = [proc.info for proc in psutil.process_iter(['pid', 'name'])]
    return processes

def get_disk_space():
    disk_usage = psutil.disk_usage('/')
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free,
        'percent': disk_usage.percent,
    }

def get_uptime():
    boot_time = time.time() - psutil.boot_time()
    return boot_time

@app.route('/request', methods=['GET'])
def service_info():

    service1_ip_address = get_ip_address()
    service1_running_process = get_running_processes()
    service1_disk_space = get_disk_space()
    service1_uptime = get_uptime()

    service1_data = {
        'IP Address': get_ip_address(),
        'Running Processes': get_running_processes(),
        'Disk Space': get_disk_space(),
        'Uptime (seconds)': get_uptime(),
    }

    try: 
        service2_response = requests.get('http://service2:3000/')
        service2_data = service2_response.json()
    except Exception as e:
        service2_data = f"Error"

    info = {
        'service 1': service1_data,
        'service 2': service2_data
    }

    time.sleep(2)

    return jsonify(info)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/stop', methods=['GET'])
def stop_system():
    client = docker.from_env()
    for container in client.containers.list():
        print(container.name)
        if "devops-tests" not in container.image.tags:
            container.stop()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)