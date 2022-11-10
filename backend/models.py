from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import VARCHAR, Unicode, UnicodeText, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.config import Config
from backend.database import Base


class ProblemLevel:
    Easy = 'Easy'
    Middle = 'Middle'
    Hard = 'Hard'


@dataclass()
class Problem(Base):
    __tablename__ = 'problem'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Unicode(80), nullable=False)
    level: Mapped[str] = mapped_column(VARCHAR(20), nullable=False,  default=ProblemLevel.Easy)
    ac_num: Mapped[int] = mapped_column(nullable=False,  default=0)
    submit_num: Mapped[int] = mapped_column(nullable=False,  default=0)
    # 一段markdown文本, 包含题目描述, 输入输出格式, 样例等内容
    description: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    # 时间空间限制
    time_limit: Mapped[int] = mapped_column(nullable=False,  default=1000)  # ms
    memory_limit: Mapped[int] = mapped_column(nullable=False,  default=10240)  # KB


@dataclass()
class Contest(Base):
    __tablename__ = 'contest'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Unicode(80), nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)


@dataclass()
class ContestProblem(Base):
    __tablename__ = 'contest_problem'
    contest_id: Mapped[int] = mapped_column(ForeignKey(Contest.id), primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey(Problem.id), primary_key=True)


@dataclass()
class User(Base):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(VARCHAR(Config.USERNAME_MAX_LEN), primary_key=True)
    password: Mapped[str] = mapped_column(VARCHAR(Config.PWD_HASHED_LEN), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(Config.EMAIL_MAX_LEN), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False,  default=False)


@dataclass()
class UserProblemPassed(Base):
    __tablename__ = 'user_problem_passed'
    username: Mapped[str] = mapped_column(ForeignKey(User.username), primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey(Problem.id), primary_key=True)


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


class SubmissionCompiler:
    GCC = 'GCC'
    GPP = 'GPP'


@dataclass()
class Submission(Base):
    __tablename__ = 'submission'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    submission_time: Mapped[datetime] = mapped_column(nullable=False,  default=datetime.now)
    username: Mapped[str] = mapped_column(ForeignKey(User.username), nullable=False)
    problem_id: Mapped[int] = mapped_column(ForeignKey(Problem.id), nullable=False)
    compiler: Mapped[str] = mapped_column(
        VARCHAR(80), nullable=False, default=SubmissionCompiler.GCC)  # 隐含了语言信息, 可用编译器在Compilers设置
    status: Mapped[str] = mapped_column(VARCHAR(80), nullable=False,  default=SubmissionStatus.Waiting)
    time_cost: Mapped[int] = mapped_column(nullable=False,  default=-1)  # ms
    memory_cost: Mapped[int] = mapped_column(nullable=False,  default=-1)  # KB
