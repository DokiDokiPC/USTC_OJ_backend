from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import VARCHAR, Unicode, UnicodeText, ForeignKey, Column

from backend.config import Config
from backend.database import Base


class ProblemLevel:
    Easy = 'Easy'
    Middle = 'Middle'
    Hard = 'Hard'


@dataclass()
class Problem(Base):
    __tablename__ = 'problem'
    id: int = Column(primary_key=True)
    name: str = Column(Unicode(80), nullable=False)
    level: str = Column(VARCHAR(20), nullable=False,  default=ProblemLevel.Easy)
    ac_num: int = Column(nullable=False,  default=0)
    submit_num: int = Column(nullable=False,  default=0)
    # 一段markdown文本, 包含题目描述, 输入输出格式, 样例等内容
    description: str = Column(UnicodeText, nullable=False)
    # 时间空间限制
    time_limit: int = Column(nullable=False,  default=1000)  # ms
    memory_limit: int = Column(nullable=False,  default=10240)  # KB


@dataclass()
class Contest(Base):
    __tablename__ = 'contest'
    id: int = Column(primary_key=True)
    name: str = Column(Unicode(80), nullable=False)
    start_time: datetime = Column(nullable=False)
    end_time: datetime = Column(nullable=False)


@dataclass()
class ContestProblem(Base):
    __tablename__ = 'contest_problem'
    contest_id: int = Column(ForeignKey(Contest.id), primary_key=True)
    problem_id: int = Column(ForeignKey(Problem.id), primary_key=True)


@dataclass()
class User(Base):
    __tablename__ = 'user'
    username: str = Column(VARCHAR(Config.USERNAME_MAX_LEN), primary_key=True)
    password: str = Column(VARCHAR(Config.PWD_HASHED_LEN), nullable=False)
    email: str = Column(VARCHAR(Config.EMAIL_MAX_LEN), nullable=False, unique=True)
    is_admin: bool = Column(nullable=False,  default=False)


@dataclass()
class UserProblemPassed(Base):
    __tablename__ = 'user_problem_passed'
    username: str = Column(ForeignKey(User.username), primary_key=True)
    problem_id: int = Column(ForeignKey(Problem.id), primary_key=True)


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
    id: int = Column(primary_key=True)
    submission_time: datetime = Column(nullable=False,  default=datetime.now)
    username: str = Column(ForeignKey(User.username), nullable=False)
    problem_id: int = Column(ForeignKey(Problem.id), nullable=False)
    compiler: str = Column(
        VARCHAR(80), nullable=False, default=SubmissionCompiler.GCC)  # 隐含了语言信息, 可用编译器在Compilers设置
    status: str = Column(VARCHAR(80), nullable=False,  default=SubmissionStatus.Waiting)
    time_cost: int = Column(nullable=False,  default=-1)  # ms
    memory_cost: int = Column(nullable=False,  default=-1)  # KB
