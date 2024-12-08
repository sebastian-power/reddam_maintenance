from flask import Flask, g
import os
import mysql.connector


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    @app.before_request
    def before_request():
        g.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("DB_PWD"),
            database=os.getenv("DB_NAME")
        )
    
    @app.teardown_request
    def teardown_request(exception=None):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
