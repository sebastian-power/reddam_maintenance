import logging
import uuid
import time
from flask import Flask, request, g
from flask_login import LoginManager
from .queries import find_user_by_id


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)

    @app.before_request
    def log_request_info():
        g.request_id = str(uuid.uuid4())
        request.start_time = time.time()  # Track request processing time

        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        user_agent = request.user_agent.string

        if request.content_length and request.content_length < 500:  # Avoid logging large bodies
            request_body = request.get_data(as_text=True)
        else:
            request_body = "[Request body too large or empty]"

        logger.info(f"""🟢 REQUEST: {g.request_id} - Client IP: {client_ip}  - User-Agent: {user_agent} - Method: {request.method} - URL: {request.url} - Body: {request_body} """)

    @app.after_request
    def log_response_info(response):
        elapsed_time = time.time() - request.start_time  # Calculate response time
        logger.info(f""" 🔴 RESPONSE: {g.request_id} - Status: {response.status_code} - Response Time: {elapsed_time:.4f}s - MIME Type: {response.mimetype} """)
        return response

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    @login_manager.user_loader
    def load_user(user_id):
        return find_user_by_id(user_id)

    from app.routes import main_bp
    from app.api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
