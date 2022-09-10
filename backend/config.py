from datetime import timedelta
from pathlib import Path

import toml
from argon2 import PasswordHasher

def get_hashed_password_len():
    ph = PasswordHasher()
    return len(ph.hash(''))

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
    
    # flask-sqlalchemy配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_SQLALCHEMY_DATABASE_URI(
        toml_path=(Path(__file__).parent / 'database_config.toml').resolve()
    )

    # flask-jwt-extended配置, JWT_SECRET_KEY默认使用SECRET_KEY
    JWT_COOKIE_SECURE = False  # 若为True, 强制使用https, 生产环境应该开启
    JWT_SESSION_COOKIE = False  # 设置为True时, cookie的expires/Max-Age为Session
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_WITHIN_HOURS = timedelta(hours=0.5)  # 在里到期的多少时间内才会更新token
    JWT_COOKIE_CSRF_PROTECT = False  # 待研究

    # 用户信息要求
    USERNAME_MIN_LEN = 2
    USERNAME_MAX_LEN = 128
    PWD_MIN_LEN = 8
    PWD_MAX_LEN = 256
    PWD_HASHED_LEN = get_hashed_password_len()
    EMAIL_MAX_LEN = 128
    NICKNAME_MIN_LEN = -1
    NICKNAME_MAX_LEN = 128
    
    # flask-wtf配置
    WTF_CSRF_ENABLED = False
    
    # flask-cors配置
    CORS_SUPPORTS_CREDENTIALS = True  # 允许传递和设置cookie

    # flask-admin配置
    FLASK_ADMIN_SWATCH = 'simplex'  # bootswatch theme
    
    # 查询分页配置
    QUERY_LIMIT = 10


Config = BaseConfig


def get_config(key):
    return getattr(Config, key, None)
