from setuptools import setup

setup(
    name='backend',
    packages=['backend'],
    include_package_data=True,
    install_requires=[
        'argon2-cffi',
        'Flask',
        'Flask_Admin',
        'Flask_Cors',
        'Flask-JWT-Extended',
        'Flask_SQLAlchemy',
        'Flask_WTF',
        'setuptools',
        'SQLAlchemy',
        'toml',
        'WTForms',
        'email-validator',
        'pika',
    ]
)
