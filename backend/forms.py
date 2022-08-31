from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, Regexp

from backend.config import get_config


class UpdateForm(FlaskForm):
    password = StringField('密码', validators=[
        DataRequired('密码不能为空'),
        Length(get_config('PWD_MIN_LEN'), get_config('PWD_MAX_LEN'), message='密码长度应在%(min)d到%(max)d之间'),
        Regexp(r'.*[0-9].*', message='密码至少包含一个数字'),
        Regexp(r'.*[a-zA-Z].*', message='密码至少包含一个字母'),
    ])


class LoginForm(UpdateForm):
    username = StringField('用户名', validators=[
        DataRequired('用户名不能为空'),
        Length(get_config('USERNAME_MIN_LEN'), get_config('USERNAME_MAX_LEN'), '用户名长度应在%(min)d到%(max)d之间')
    ])


class RegisterForm(LoginForm):
    email = StringField('邮箱', validators=[
        DataRequired('邮箱不能为空'),
        Email('邮箱格式错误')
    ])
