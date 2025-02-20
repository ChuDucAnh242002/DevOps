import pytest
import requests
import docker
import time

BASE_URL = "http://nginx:8197"

def test_service_info():
    url = BASE_URL + "/request"
    response = requests.get(url)

    assert response.status_code == 200

    data = response.json()
    assert 'service 1' in data
    assert 'service 2' in data

    service1_data = data['service 1']
    assert 'IP Address' in service1_data
    assert 'Running Processes' in service1_data
    assert 'Disk Space' in service1_data
    assert 'Uptime (seconds)' in service1_data 

    assert isinstance(service1_data['IP Address'], str)
    assert isinstance(service1_data['Running Processes'], list)
    assert isinstance(service1_data['Disk Space'], dict)
    assert isinstance(service1_data['Uptime (seconds)'], float)

    disk_space = service1_data['Disk Space']
    assert 'total' in disk_space
    assert 'used' in disk_space
    assert 'free' in disk_space
    assert 'percent' in disk_space

    assert isinstance(disk_space['total'], int)
    assert isinstance(disk_space['used'], int)
    assert isinstance(disk_space['free'], int)
    assert isinstance(disk_space['percent'], float)

def test_home():
    url = BASE_URL
    response = requests.post(url)

    assert response.status_code == 200
    assert "Home" in response.text
    assert "<form action=\"/request\" method=\"get\">" in response.text
    assert "<form action=\"/stop\" method=\"post\">" in response.text
    assert "<textarea id=\"output\" rows=\"10\" cols=\"50\"></textarea>" in response.text

def test_get_state():
    url = BASE_URL + "/state"
    session = requests.Session()

    response = session.post(BASE_URL)
    assert response.status_code == 200

    response = session.get(url)

    assert response.status_code == 200
    assert response.text == "RUNNING"

def test_manage_state():
    url = BASE_URL + "/state"
    requests.get(BASE_URL)

    # test INIT state
    response = requests.put(url, data="INIT")
    assert response.status_code == 200
    assert response.text == "INIT"

    # test RUNNING state
    response = requests.put(url, data="RUNNING")
    assert response.status_code == 200
    assert response.text == "RUNNING"

    response = requests.put(url)
    assert response.status_code == 200
    assert response.text == "RUNNING"

    # test PAUSED state
    response = requests.put(url, data="PAUSED", headers=headers)
    assert response.status_code == 200
    assert response.text == "PAUSED"

    response = requests.put(url)
    assert response.status_code == 200
    assert response.text == "PAUSED"

    # test SHUTDOWN state
    response = requests.put(url, data="SHUTDOWN", headers=headers)
    assert response.status_code == 200
    assert response.text == "SHUTDOWN"

    response = requests.put(url)
    assert response.status_code == 200
    assert response.text == "SHUTDOWN"

def test_get_run_log():
    url = BASE_URL + "/run-log"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/plain'
    assert ("INIT->RUNNING" in response.text) or ("RUNNING->PAUSED" in response.text) or ("PAUSED->RUNNING" in response.text)

# def test_stop_system():
#     client = docker.from_env()

#     url = BASE_URL + "/stop"
#     response = requests.get(url, auth=(USERNAME, PASSWORD))
#     assert response.status_code == 200  
    # time.sleep(60)

    # container_list = client.containers.list()
    
    # assert len(container_list) == 1
