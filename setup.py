from setuptools import setup

setup(
    name='backend',
    packages=['backend'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask_Admin',
        'Flask_Cors',
        'Flask_SQLAlchemy',
        'Flask_WTF',
        'PyJWT',
        'setuptools',
        'SQLAlchemy',
        'toml',
        'WTForms',
        'email-validator'
    ]
)
