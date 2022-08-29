# 数据库信息, 也应放在.env文件中
USERNAME = 'root'
PASSWORD = '1234'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'ustcoj'

class BaseConfig(object):
    SECRET_KEY = 'secret'
    
    # flask-sqlalchemy配置
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    
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

def getc(key):
    return getattr(Config, key, None)
