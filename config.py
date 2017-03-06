import os
import pymysql

class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'data.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/datadb?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # DATABASE = '/tmp/test.db'
    TESTING = False
    DEBUG = False
    SECRET_KEY = 'deployment key'
    USERNAME = 'admin'
    PASSWORD = '123'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    TESTING = True
