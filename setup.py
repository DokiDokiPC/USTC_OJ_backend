from setuptools import setup

setup(
    name='backend',
    version='0.0.1',
    packages=['backend'],
    install_requires=[
        'argon2-cffi==21.3.0',
        'Flask==2.3.2',
        'Flask_Admin==1.6.1',
        'Flask_Cors==3.0.10',
        'Flask_JWT_Extended==4.4.4',
        'Flask_WTF==1.1.1',
        'SQLAlchemy==2.0.13',
        'pymysql==1.0.3',
        'toml==0.10.2',
        'WTForms==3.0.1',
        'email-validator==2.0.0',
        'pika==1.3.2',
    ]
)
