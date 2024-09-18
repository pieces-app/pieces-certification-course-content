# config.py
class Config:
    TESTING = False
    DEBUG = False

class TestConfig(Config):
    TESTING = True
    DEBUG = True
