# tests/conftest.py
import pytest
from flask import Flask
from flask_login import LoginManager, login_user
from app.api import api_bp
from unittest.mock import patch

class TestUser:
    def __init__(self, id=1, role='Admin'):
        self.user_id = id
        self.role = role
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.user_id)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.config['LOGIN_DISABLED'] = False
    
    # Register the blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return TestUser(id=int(user_id))
        
    return app

@pytest.fixture
def test_client(app):
    return app.test_client()

@pytest.fixture
def auth_client(app, test_client):
    user = TestUser(role='Admin')  # Explicitly set admin role
    with app.test_request_context():
        login_user(user)
    
    with test_client.session_transaction() as session:
        session['_user_id'] = '1'
        session['_fresh'] = True
    
    return test_client

@pytest.fixture
def unauth_client(app, test_client):
    user = TestUser(role='User')  # Create user with non-admin role
    with app.test_request_context():
        login_user(user)
    
    with test_client.session_transaction() as session:
        session['_user_id'] = '1'
        session['_fresh'] = True
    
    return test_client

@pytest.fixture
def worker_client(app, test_client):
    user = TestUser(role='Worker')  # Create user with worker role
    with app.test_request_context():
        login_user(user)
    
    with test_client.session_transaction() as session:
        session['_user_id'] = '1'
        session['_fresh'] = True
    
    return test_client