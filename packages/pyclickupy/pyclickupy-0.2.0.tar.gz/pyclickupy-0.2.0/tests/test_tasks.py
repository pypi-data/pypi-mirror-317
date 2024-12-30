import pytest
from pyclickupy import ClickUpClient
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

@pytest.fixture
def mock_task_response():
    return {
        "id": "task123",
        "name": "Test Task",
        "description": "Test Description",
        "status": {
            "status": "to do",
            "color": "#d3d3d3"
        },
        "priority": None,
        "assignees": [],
        "due_date": None
    }

def test_get_task(client, mock_task_response):
    with patch('requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = mock_task_response
        mock_get.return_value.headers = {
            "x-ratelimit-remaining": "100",
            "x-ratelimit-reset": str(int(datetime.now().timestamp()))
        }

        task = client.get_task("task123")
        assert task.id == "task123"
        assert task.name == "Test Task"
        assert task.description == "Test Description"

def test_create_task(client, mock_task_response):
    with patch('requests.post') as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = mock_task_response
        
        task = client.create_task(
            list_id="list123",
            name="Test Task",
            description="Test Description"
        )
        
        assert task.id == "task123"
        assert task.name == "Test Task"

def test_update_task(client, mock_task_response):
    with patch('requests.put') as mock_put:
        mock_put.return_value.ok = True
        mock_put.return_value.json.return_value = mock_task_response
        
        task = client.update_task(
            task_id="task123",
            name="Updated Task",
            description="Updated Description"
        )
        
        assert task.id == "task123"

def test_delete_task(client):
    with patch('requests.delete') as mock_delete:
        mock_delete.return_value.ok = True
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {"ok": True}
        
        result = client.delete_task("task123")
        assert result == True 