from datetime import datetime, timezone, timedelta
from http import HTTPStatus

from flask import render_template
from sqlalchemy import exc
import jwt

from backend import app
from backend.config import getc
from backend.models import db, User
from backend.forms import LoginForm, RegisterForm

# GET: 登录页面
# POST: 传入用户名和密码, 验证是否正确, 若正确则返回JWT, 否则返回UNAUTHORIZED
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            return render_template('login.html', form=form, err_msg=f'用户{form.username.data}不存在'),\
                   HTTPStatus.UNAUTHORIZED
        if form.password.data != user.password:
            return render_template('login.html', form=form, err_msg=f'密码错误'), HTTPStatus.UNAUTHORIZED
        return jwt.encode(
            {
                'exp': datetime.now(tz=timezone.utc) + timedelta(hours=getc('JWT_EXP_HOURS')),
                'username': form.username.data
            },
            getc('JWT_SECRET'),
            getc('JWT_ALGORITHM')
        )
    return render_template('login.html', form=form)

# GET: 注册页面
# POST: 传入用户名, 密码, 邮箱和昵称(可选), 新建账户
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            return render_template('register.html', form=form, err_msg=f'用户{form.username.data}已存在'), HTTPStatus.CONFLICT
        if User.query.filter_by(email=form.email.data).first():
            return render_template('register.html', form=form, err_msg=f'邮箱{form.email.data}已存在'), HTTPStatus.CONFLICT
        new_user = User(username=form.username.data, password=form.password.data,
                        email=form.email.data, nickname=form.nickname.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return '注册成功', HTTPStatus.CREATED
        except exc.SQLAlchemyError:
            return render_template('register.html', form=form, err_msg=f'SQLAlchemyError'), HTTPStatus.NOT_ACCEPTABLE
    return render_template('register.html', form=form)
