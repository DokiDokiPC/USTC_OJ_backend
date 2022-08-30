from dataclasses import dataclass

from backend.config import get_config
from backend.db import db


@dataclass
class Problem(db.Model):
    ID: int = db.Column(db.Integer, primary_key=True)
    Title: str = db.Column(db.String(80), nullable=False)


@dataclass
class User(db.Model):
    ID: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(get_config('USERNAME_MAX_LEN')), nullable=False, unique=True)
    password: str = db.Column(db.String(get_config('PWD_MAX_LEN')), nullable=False)
    email: str = db.Column(db.String(get_config('EMAIL_MAX_LEN')), nullable=False, unique=True)
    nickname: str = db.Column(db.String(get_config('NICKNAME_MAX_LEN')), nullable=False)
