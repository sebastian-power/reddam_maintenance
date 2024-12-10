import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
class DevConfig(Config):
    DEBUG = True
    TESTING = True
class ProdConfig(Config):
    # For production (running final product)
    pass
