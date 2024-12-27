import os
from dotenv import load_dotenv
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    REMEMBER_COOKIE_DURATION = timedelta(days=180)
class DevConfig(Config):
    DEBUG = True
    TESTING = True
class ProdConfig(Config):
    # For production (running final product)
    pass
