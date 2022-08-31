from datetime import timedelta
from pathlib import Path

import toml


def get_SQLALCHEMY_DATABASE_URI(toml_path):
    database_config = toml.load(toml_path)
    USERNAME = database_config['USERNAME']
    PASSWORD = database_config['PASSWORD']
    HOSTNAME = database_config['HOSTNAME']
    PORT = database_config['PORT']
    DATABASE = database_config['DATABASE_NAME']
    return f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'


class BaseConfig(object):
    # flask密钥
    SECRET_KEY = 'secret'
    
    # sqlalchemy配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_SQLALCHEMY_DATABASE_URI(
        toml_path=(Path(__file__).parent / 'database_config.toml').resolve()
    )

    # jwt配置, JWT_SECRET_KEY默认使用SECRET_KEY
    JWT_COOKIE_SECURE = False  # 若为True, 强制使用https, 生产环境应该开启
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_WITHIN_HOURS = timedelta(hours=0.5)  # 在里到期的多少时间内才会更新token
    JWT_COOKIE_CSRF_PROTECT = False

    # 用户信息要求
    USERNAME_MIN_LEN = 6
    USERNAME_MAX_LEN = 80
    PWD_MIN_LEN = -1
    PWD_MAX_LEN = 200
    EMAIL_MAX_LEN = 120
    NICKNAME_MIN_LEN = -1
    NICKNAME_MAX_LEN = 80

    # flask-docs配置
    API_DOC_MEMBER = ['problem', 'user', 'token', 'status']
    
    # flask-wtf配置
    WTF_CSRF_ENABLED = False
    
    # flask-admin配置
    FLASK_ADMIN_SWATCH = 'simplex'  # bootswatch theme


Config = BaseConfig


def get_config(key):
    return getattr(Config, key, None)
