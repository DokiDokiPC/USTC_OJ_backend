from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, Regexp

from backend.config import get_config
from backend import app

# 注册CSRF扩展 有了jwt还需不需要csrf?
# csrf = CSRFProtect(app)

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(get_config('USERNAME_MIN_LEN'), get_config('USERNAME_MAX_LEN'), '用户名长度应在%(min)d到%(max)d之间')
    ])
    password = StringField('密码', validators=[
        DataRequired(),
        Length(get_config('PWD_MIN_LEN'), get_config('PWD_MAX_LEN'), message='用户名长度应在%(min)d到%(max)d之间'),
        Regexp(r'.*[0-9].*', message='密码至少包含一个数字'),
        Regexp(r'.*[a-zA-Z].*', message='密码至少包含一个字母'),
    ])
    
class RegisterForm(LoginForm):
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email('邮箱格式错误')
    ])
    nickname = StringField('昵称', validators=[
        Length(get_config('NICKNAME_MIN_LEN'), get_config('NICKNAME_MAX_LEN'))
    ])
