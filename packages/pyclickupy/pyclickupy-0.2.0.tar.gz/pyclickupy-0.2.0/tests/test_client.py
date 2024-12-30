import pytest
from pyclickupy import ClickUpClient, ClickupClientError
from datetime import datetime

def test_client_initialization(mock_token):
    client = ClickUpClient(accesstoken=mock_token)
    assert client.accesstoken == mock_token
    assert client.api_url == "https://api.clickup.com/api/v2/"
    assert client.request_count == 0
    assert client.default_space is None
    assert client.default_list is None
    assert client.default_task is None

def test_client_custom_initialization(mock_token):
    custom_url = "https://custom-api.clickup.com/v2/"
    client = ClickUpClient(
        accesstoken=mock_token,
        api_url=custom_url,
        default_space="space123",
        default_list="list123",
        default_task="task123",
        retry_rate_limited_requests=True,
        rate_limit_buffer_wait_time=10
    )
    
    assert client.api_url == custom_url
    assert client.default_space == "space123"
    assert client.default_list == "list123"
    assert client.default_task == "task123"
    assert client.rate_limit_buffer_wait_time == 10
    assert client.retry_rate_limited_requests == True

def test_headers_generation(client):
    headers = client._ClickUpClient__headers()
    assert headers["Authorization"] == "test_token_12345"
    assert headers["Content-Type"] == "application/json"

    file_headers = client._ClickUpClient__headers(file_upload=True)
    assert file_headers["Authorization"] == "test_token_12345"
    assert "Content-Type" not in file_headers 