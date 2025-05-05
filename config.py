import os
import socket
from dotenv import load_dotenv
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))
os.environ["WEBSITE_DOMAIN"] = f"{socket.gethostbyname(socket.gethostname())}:5000"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    REMEMBER_COOKIE_DURATION = timedelta(days=180)
    SESSION_COOKIE_SAMESITE = "Strict"
class DevConfig(Config):
    DEBUG = True
    TESTING = True
class ProdConfig(Config):
    pass
