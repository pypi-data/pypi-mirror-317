import pytest
from pyclickupy import ClickUpClient

@pytest.fixture
def mock_token():
    return "test_token_12345"

@pytest.fixture
def client(mock_token):
    return ClickUpClient(
        accesstoken=mock_token,
        retry_rate_limited_requests=True
    ) 