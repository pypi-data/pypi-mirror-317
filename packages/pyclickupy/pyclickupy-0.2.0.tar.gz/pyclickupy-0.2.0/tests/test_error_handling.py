import pytest
from pyclickupy import ClickUpClient, ClickupClientError
from unittest.mock import patch
from datetime import datetime

def test_invalid_token(mock_token):
    with patch('requests.get') as mock_get:
        mock_get.return_value.ok = False
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {"err": "Invalid token"}
        mock_get.return_value.headers = {
            "x-ratelimit-remaining": "100",
            "x-ratelimit-reset": str(int(datetime.now().timestamp()))
        }

        client = ClickUpClient(accesstoken=mock_token)
        
        with pytest.raises(ClickupClientError) as exc_info:
            client.get_task("task123")
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.error_message == "Invalid token"

def test_rate_limit_handling(mock_token):
    with patch('requests.get') as mock_get:
        mock_get.return_value.ok = False
        mock_get.return_value.status_code = 429
        mock_get.return_value.json.return_value = {"err": "Rate limit exceeded"}
        mock_get.return_value.headers = {
            "x-ratelimit-remaining": "0",
            "x-ratelimit-reset": str(int(datetime.now().timestamp()) + 60)
        }

        client = ClickUpClient(
            accesstoken=mock_token,
            retry_rate_limited_requests=False
        )
        
        with pytest.raises(ClickupClientError) as exc_info:
            client.get_task("task123")
        
        assert exc_info.value.status_code == 429
        assert "Rate limit exceeded" in str(exc_info.value) 