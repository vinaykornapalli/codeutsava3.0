import os
basedir = os.path.abspath(os.path.dirname(__file__))

config = {
  'ORIGINS': [
    'http://localhost:8080',  # React
    'http://127.0.0.1:8080',  # React
  ],

  'SECRET_KEY': '...'
}

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '111'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True