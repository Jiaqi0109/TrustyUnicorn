import os
from redis import Redis


class Config:

    # 密钥，提交表单需要
    SECRET_KEY = '123456'

    ADMIN_AUTH = '000000'

    # 配置redis作为session服务器
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='localhost', port='6379', db=0)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_ECHO = False

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    UPLOADED_PATH = os.path.join(BASE_DIR, 'app/static/upload')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:jiaqi0109@localhost/lagou0508'
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    JSON_SORT_KEYS = False
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    DEBUG = False
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
