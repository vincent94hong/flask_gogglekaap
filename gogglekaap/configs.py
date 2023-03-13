import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config:
    '''Flask Config'''
    SECRET_KEY = 'secretkey'
    SESSION_COOKIE_NAME = 'gogglekaap'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLALCHEMY_TRACK_MODIFICATIONS 에러발생시 설정.
    SWAGGER_UI_DOC_EXPANSION = 'list'
    USER_STATIC_BASE_DIR = 'user_images'

class DevelopmentConfig(Config):
    '''Flask Config for dev'''
    DEBUG = True
    SEND_FIND_MAX_DEFAULT = 1
    # TODO: Front 호출시 처리
    WTF_CSRF_ENABLED = False

class TestingConfig(DevelopmentConfig):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}'

class ProductionConfig(Config):
    pass