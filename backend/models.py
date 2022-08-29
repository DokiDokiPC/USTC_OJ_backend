from flask_sqlalchemy import SQLAlchemy

from backend.config import getc

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(getc('USERNAME_MAX_LEN')), unique=True, nullable=False)
    password = db.Column(db.String(getc('PWD_MAX_LEN')), nullable=False)
    email = db.Column(db.String(getc('EMAIL_MAX_LEN')), unique=True, nullable=False)
    nickname = db.Column(db.String(getc('NICKNAME_MAX_LEN')), nullable=False)
