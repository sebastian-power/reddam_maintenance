from flask import Flask
from flask_login import LoginManager
from .queries import find_user_by_id


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

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
