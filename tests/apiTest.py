from service1.app import app, service_info, login, home
import pytest
from flask import Flask, jsonify, render_template_string
import requests
import docker
from unittest.mock import patch, MagicMock

@pytest.fixture
def client(app):
    return app.test_client()


def test_service_info(client, requests_mock):
    requests_mock.get('http://service2:3000/', json={'status': 'ok'})

    # Make a request to get the /request endpoint
    response = client.get('/request')
    data = response.get_json()

    assert response.status_code = 200
    assert 'service 1' in data
    assert 'service 2' in data
    assert data['service 1']['IP Address'] == "192.168.1.1"
    assert data['service 2'] == {'status': 'ok'}

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_stop_system(client, mocker):
    mock_docker = mocker.patch('docker.from_env')
    mock_client = MagicMock()
    mock_container = MagicMock()
    mock_docker.return_value = mock_client
    mock_client.containers.list.return_value = [mock_container]

    # Make a request to the /stop endpoint
    response = client.get('/stop')

    # Assert the response and that the container.stop() method was called
    assert response.status_code == 200
    assert response.data.decode() == "System shutting down."
    mock_container.stop.assert_called_once()