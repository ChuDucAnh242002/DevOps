import pytest
import requests
# from unittest.mock import patch, MagicMock

BASE_URL = "http://nginx:80"
USERNAME = "user1"
PASSWORD = "123456"

def test_service_info():
    url = BASE_URL + "/request"
    response = requests.get(url, auth=(USERNAME, PASSWORD))

    assert response.status_code == 200

def test_login():
    url = BASE_URL + "/login"
    response = requests.get(url, auth=(USERNAME, PASSWORD))

    assert response.status_code == 200

def test_home():
    url = BASE_URL
    response = requests.get(url, auth=(USERNAME, PASSWORD))

    assert response.status_code == 200

# def test_stop_system():
#     url = BASE_URL + "/stop"
#     response = requests.get(url, auth=(USERNAME, PASSWORD))

#     assert response.status_code == 200  
