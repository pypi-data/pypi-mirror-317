import pytest
from pyclickupy import ClickUpClient
from unittest.mock import patch
from datetime import datetime


@pytest.fixture
def mock_list_response():
    return {
        "id": "list123",
        "name": "Test List",
        "content": "Test Content",
        "status": {
            "status": "active",
            "color": "#000000"
        },
        "priority": None,
        "assignee": {
            "id": None,
            "username": None,
            "email": None,
            "color": None,
            "initials": None,
            "profilePicture": None
        },
        "task_count": 0
    }

def test_get_list(client, mock_list_response):
    with patch('requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = mock_list_response
        mock_get.return_value.headers = {
            "x-ratelimit-remaining": "100",
            "x-ratelimit-reset": str(int(datetime.now().timestamp()))
        }

        list_obj = client.get_list("list123")
        assert list_obj.id == "list123"
        assert list_obj.name == "Test List"
        assert list_obj.content == "Test Content"

def test_create_list(client, mock_list_response):
    with patch('requests.post') as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = mock_list_response
        
        list_obj = client.create_folderless_list(
            space_id="space123",
            name="Test List",
            content="Test Content"
        )
        
        assert list_obj.id == "list123"
        assert list_obj.name == "Test List"

def test_delete_list(client):
    with patch('requests.delete') as mock_delete:
        mock_delete.return_value.ok = True
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {"ok": True}
        
        result = client.delete_list("list123")
        assert result == True 