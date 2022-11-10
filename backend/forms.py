from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms.widgets import PasswordInput

from backend.config import Config


class UserUpdateForm(FlaskForm):
    password = StringField('Password', validators=[
        DataRequired('Password can not be blank'),
        Length(Config.PWD_MIN_LEN, Config.PWD_MAX_LEN,
               message='Password length should between %(min)d and %(max)d'),
        # ^代表开头, $代表结尾, \S匹配非空字符, re.match尝试从开头寻找一个匹配, 所以不用加^
        Regexp(r'\S+$', message='Password can not contain whitespace characters'),
        Regexp(r'.*[0-9]', message='Password should contain at least 1 number'),
        Regexp(r'.*[a-zA-Z]', message='Password should contain at least 1 letter'),
    ], widget=PasswordInput(hide_value=False))


class LoginForm(UserUpdateForm):
    username = StringField('Username', validators=[
        DataRequired('Username can not be blank'),
        Length(Config.USERNAME_MIN_LEN, Config.USERNAME_MAX_LEN,
               message='Username length should between %(min)d and %(max)d'),
        Regexp(r'\w+$', message='Username can only consist of letters, numbers or underscores'),
    ])


class RegisterForm(LoginForm):
    email = StringField('Email', validators=[
        DataRequired('Email can not be blank'),
        Email('Email format error')
    ])


class SubmissionForm(FlaskForm):
    problem_id = IntegerField('Problem ID', validators=[
        DataRequired('Problem ID can not be blank')
    ])
    compiler = StringField('Compiler', validators=[
        DataRequired('Compiler can not be blank')
    ])
    source_code = StringField('Source code', validators=[
        DataRequired('Source code can not be blank'),
        Length(max=2**18, message='Source code size should be within 256KB')
    ])


class ProblemForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired('Name can not be blank')
    ])
    level = StringField('Level')
    description = StringField('Description', validators=[
        DataRequired('Description can not be blank')
    ])
    time_limit = IntegerField('Time Limit', validators=[
        DataRequired('Time Limit can not be blank')
    ])
    memory_limit = IntegerField('Memory Limit', validators=[
        DataRequired('Memory Limit can not be blank')
    ])
