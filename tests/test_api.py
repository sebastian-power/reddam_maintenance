# tests/test_api.py
import pytest
from flask import json
from unittest.mock import patch, MagicMock
from app.api import api_bp
from flask_login import login_user

def encrypt_id(task_id):
    encoded = str(task_id * 13087137435673)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return ''.join(alphabet[int(digit)] for digit in encoded)

class TestChangeStatusDrag:
    @patch('app.api.update_task_status')
    @patch('app.api.find_task_by_id')
    @patch('app.api.task_completed_email')
    def test_change_status_success(self, mock_email, mock_find_task, mock_update, app, auth_client):
        task_id = 123
        encoded_id = encrypt_id(task_id)
        mock_task = MagicMock()
        mock_find_task.return_value = mock_task
        
        with app.test_request_context():
            response = auth_client.post('/api/change_status_drag',
                json={'encoded_value': encoded_id, 'new_status': 'Done'})
        
        assert response.status_code == 200
        assert response.data == b"Status updated"
        mock_update.assert_called_once_with(task_id, 'Done')
        mock_email.assert_called_once_with(mock_task)

    @patch('app.api.update_task_status')
    @patch('app.api.task_completed_email')
    def test_change_status_not_done(self, mock_email, mock_update, app, auth_client):
        task_id = 123
        encoded_id = encrypt_id(task_id)
        
        with app.test_request_context():
            response = auth_client.post('/api/change_status_drag',
                json={'encoded_value': encoded_id, 'new_status': 'In Progress'})
        
        assert response.status_code == 200
        assert response.data == b"Status updated"
        mock_update.assert_called_once_with(task_id, 'In Progress')
        mock_email.assert_not_called()

class TestGetTasksSorted:
    @patch('app.api.retrieve_tasks')
    def test_get_tasks_sorted_success(self, mock_retrieve, app, auth_client):
        mock_tasks = [
            {'id': 1, 'title': 'Task 1'},
            {'id': 2, 'title': 'Task 2'}
        ]
        mock_retrieve.return_value = mock_tasks
        
        with app.test_request_context():
            response = auth_client.post('/api/get_tasks_sorted',
                json={'sort_method': 'date'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['tasks'] == mock_tasks
        mock_retrieve.assert_called_once_with(sort_by='date')

class TestDeleteTask:
    @patch('app.api.delete_task_query')
    def test_delete_task_success(self, mock_delete, app, auth_client):
        task_id = 123
        encoded_id = encrypt_id(task_id)
        
        with app.test_request_context():
            response = auth_client.post('/api/delete_task',
                json={'encoded_value': encoded_id})
        
        assert response.status_code == 200
        assert response.data == b"Task deleted"
        mock_delete.assert_called_once_with(task_id)

class TestGetWorkers:
    @patch('app.api.retrieve_workers')
    def test_get_workers_success(self, mock_retrieve, app, auth_client):
        mock_workers = ['Worker 1', 'Worker 2']
        mock_retrieve.return_value = mock_workers
        
        with app.test_request_context():
            response = auth_client.post('/api/get_workers')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['worker_names'] == mock_workers

class TestAssignWorker:
    @pytest.mark.parametrize('client_fixture', ['auth_client', 'worker_client'])
    @patch('app.api.assign_task')
    def test_assign_worker_authorized(self, mock_assign, app, request, client_fixture):
        client = request.getfixturevalue(client_fixture)
        task_id = 123
        encoded_id = encrypt_id(task_id)
        
        with app.test_request_context():
            response = client.post('/api/assign_worker',
                json={'encoded_value': encoded_id})
        
        assert response.status_code == 200
        assert response.data == b"Worker assigned"
        mock_assign.assert_called_once_with(task_id, 1)

    def test_assign_worker_unauthorized(self, app, unauth_client):
        task_id = 123
        encoded_id = encrypt_id(task_id)
        
        with app.test_request_context():
            response = unauth_client.post('/api/assign_worker',
                json={'encoded_value': encoded_id})
        
        assert response.status_code == 403

def test_unauthorized_access(app, test_client):
    """Test that unauthorized access returns appropriate error"""
    endpoints = [
        '/api/change_status_drag',
        '/api/get_tasks_sorted',
        '/api/delete_task',
        '/api/get_workers',
        '/api/assign_worker'
    ]
    
    for endpoint in endpoints:
        with app.test_request_context():
            response = test_client.post(endpoint, json={})
            assert response.status_code in [401, 403], f"Endpoint {endpoint} should require authentication"