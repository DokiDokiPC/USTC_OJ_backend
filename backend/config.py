import toml


def get_SQLALCHEMY_DATABASE_URI():
    database_config = toml.load("./my_database_config.toml")
    USERNAME = database_config['USERNAME']
    PASSWORD = database_config['PASSWORD']
    HOSTNAME = database_config['HOSTNAME']
    PORT = database_config['PORT']
    DATABASE = database_config['DATABASE_NAME']
    return f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'


class BaseConfig(object):
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_SQLALCHEMY_DATABASE_URI()

    # jwt配置
    JWT_SECRET = 'secret'  # 应放在.env文件中, 可在每次启动服务时随机生成
    JWT_ALGORITHM = 'HS256'
    JWT_EXP_HOURS = 0.5
    JWT_LEEWAY = 10  # 检查时间上限

    # 用户信息要求
    USERNAME_MIN_LEN = 6
    USERNAME_MAX_LEN = 80
    PWD_MIN_LEN = 8
    PWD_MAX_LEN = 80
    EMAIL_MAX_LEN = 120
    NICKNAME_MIN_LEN = -1
    NICKNAME_MAX_LEN = 80

    # wtf配置
    WTF_CSRF_ENABLED = False  # 有了jwt还需不需要csrf?


Config = BaseConfig


def get_config(key):
    return getattr(Config, key, None)
