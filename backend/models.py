from dataclasses import dataclass
from datetime import datetime

from backend.config import get_config
from backend.db import db


@dataclass
class Problem(db.Model):
    ID: int = db.Column(db.Integer, primary_key=True)
    Title: str = db.Column(db.String(80), nullable=False)
    Level: str = db.Column(db.String(20), nullable=False)
    ac_num: int = db.Column(db.Integer, nullable=False, default=0)
    submit_num: int = db.Column(db.Integer, nullable=False, default=0)


@dataclass
class User(db.Model):
    ID: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(get_config(
        'USERNAME_MAX_LEN')), nullable=False, unique=True)
    password: str = db.Column(
        db.String(get_config('PWD_MAX_LEN')), nullable=False)
    email: str = db.Column(db.String(get_config(
        'EMAIL_MAX_LEN')), nullable=False, unique=True)
    nickname: str = db.Column(
        db.String(get_config('NICKNAME_MAX_LEN')), nullable=False)


@dataclass
class Status(db.Model):
    ID: int = db.Column(db.Integer, primary_key=True)
    submitTime: datetime = db.Column(db.DateTime, nullable=False)
    problemId: int = db.Column(
        db.Integer, db.ForeignKey('problem.ID'), nullable=False,)
    coder: str = db.Column(db.String(80), db.ForeignKey(
        'user.username'), nullable=False)
    status: str = db.Column(db.String(20), nullable=False)
    timeCost: int = db.Column(db.Integer, nullable=False)
    memoryCost: int = db.Column(db.Integer, nullable=False)
