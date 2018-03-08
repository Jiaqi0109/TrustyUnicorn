import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'app/static/upload')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:jiaqi0109@localhost/lagou'
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
