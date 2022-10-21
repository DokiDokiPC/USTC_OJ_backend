from dataclasses import dataclass
from datetime import datetime

from backend.config import get_config
from backend.extensions.db import db


@dataclass
class Problem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(80), nullable=False)
    level: str = db.Column(db.String(20), nullable=False)
    ac_num: int = db.Column(db.Integer, nullable=False, default=0)
    submit_num: int = db.Column(db.Integer, nullable=False, default=0)
    # 一段markdown文本, 包含题目描述, 输入输出格式, 样例等内容
    description: str = db.Column(db.Unicode(8000), nullable=False)
    # 时间空间限制
    time_limit: int = db.Column(db.Integer, nullable=False)  # ms
    memory_limit: int = db.Column(db.Integer, nullable=False)  # KB


@dataclass
class Contest(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(80), nullable=False)
    start_time: datetime = db.Column(db.DateTime, nullable=False)
    end_time: datetime = db.Column(db.DateTime, nullable=False)


@dataclass
class ContestProblem(db.Model):
    problem_id: int = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True)
    contest_id: int = db.Column(db.Integer, db.ForeignKey('contest.id'), primary_key=True)


@dataclass
class User(db.Model):
    username: str = db.Column(db.String(get_config('USERNAME_MAX_LEN')), primary_key=True)
    password: str = db.Column(db.String(get_config('PWD_HASHED_LEN')), nullable=False)
    email: str = db.Column(db.String(get_config('EMAIL_MAX_LEN')), nullable=False, unique=True)
    is_admin: bool = db.Column(db.Boolean(), nullable=False, default=False)


@dataclass
class PassedProblem(db.Model):
    username: str = db.Column(db.String(get_config('USERNAME_MAX_LEN')),
                              db.ForeignKey('user.username'), primary_key=True)
    problem_id: int = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True)


class SubmissionStatus:
    # 初始状态
    Waiting = 'Waiting'
    # 结束状态
    CompileError = 'CompileError'
    RuntimeError = 'RuntimeError'
    MemoryLimitExceeded = 'MemoryLimitExceeded'
    TimeLimitExceeded = 'TimeLimitExceeded'
    WrongAnswer = 'WrongAnswer'
    Accepted = 'Accepted'


@dataclass
class Submission(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    submission_time: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username: str = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    problem_id: int = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    compiler: str = db.Column(db.String(80), nullable=False)  # 隐含了语言信息, 可用编译器在config.py设置
    status: str = db.Column(db.String(80), nullable=False)
    time_cost: int = db.Column(db.Integer)  # ms
    memory_cost: int = db.Column(db.Integer)  # KB
