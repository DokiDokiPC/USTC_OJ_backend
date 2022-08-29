from setuptools import setup

setup(
    name='backend',
    packages=['backend'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask_Admin',
        'Flask_SQLAlchemy',
        'Flask_WTF',
        'PyJWT',
        'SQLAlchemy',
        'SQLAlchemy-Utils'
        'WTForms',
        'email-validator'
    ]
)
