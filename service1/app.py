from flask import Flask, jsonify
import psutil
import socket
import requests
import time
import asyncio

app = Flask(__name__)

async def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return ip_address

async def get_running_processes():
    processes = [proc.info for proc in psutil.process_iter(['pid', 'name'])]
    return processes

async def get_disk_space():
    disk_usage = psutil.disk_usage('/')
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free,
        'percent': disk_usage.percent,
    }

async def get_uptime():
    boot_time = time.time() - psutil.boot_time()
    return boot_time

@app.route('/', methods=['GET'])
async def service_info():

    # service1_ip_address = await get_ip_address()
    # service1_running_process = await get_running_processes()
    # service1_disk_space = await get_disk_space()
    # service1_uptime = await get_uptime()

    service1_data = {
        'IP Address': await get_ip_address(),
        'Running Processes': await get_running_processes(),
        'Disk Space': await get_disk_space(),
        'Uptime (seconds)': await get_uptime(),
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

    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8199)