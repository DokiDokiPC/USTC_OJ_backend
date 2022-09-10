from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, Regexp

from backend.config import get_config


class UpdateForm(FlaskForm):
    password = StringField('Password', validators=[
        DataRequired('Password can not be blank'),
        Length(get_config('PWD_MIN_LEN'), get_config('PWD_MAX_LEN'),
               message='Password length should between %(min)d and %(max)d'),
        # ^代表开头, $代表结尾, \S匹配非空字符, re.match尝试从开头寻找一个匹配, 所以不用加^
        Regexp(r'\S+$', message='Password can not contain whitespace characters'),
        Regexp(r'.*[0-9]', message='Password should contain at least 1 number'),
        Regexp(r'.*[a-zA-Z]', message='Password should contain at least 1 letter'),
    ])


class LoginForm(UpdateForm):
    username = StringField('Username', validators=[
        DataRequired('Username can not be blank'),
        Length(get_config('USERNAME_MIN_LEN'), get_config('USERNAME_MAX_LEN'),
               message='Username length should between %(min)d and %(max)d'),
        Regexp(r'\w+$', message='Username can only consist of letters, numbers or underscores'),
    ])


class RegisterForm(LoginForm):
    email = StringField('Email', validators=[
        DataRequired('Email can not be blank'),
        Email('Email format error')
    ])
