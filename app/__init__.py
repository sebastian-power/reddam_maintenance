from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
