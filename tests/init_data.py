from random import randint, choice, choices
import string

from argon2 import PasswordHasher

from backend.database import Session, engine
from backend.models import *
from backend.config import Config

with Session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

N = 100


def gen_list_from_class(cls):
    _list = []
    for k, v in cls.__dict__.items():
        if not k.startswith('__'):
            _list.append(v)
    return _list


levels = gen_list_from_class(ProblemLevel)
compilers = gen_list_from_class(SubmissionCompiler)
stateses = gen_list_from_class(SubmissionStatus)

# 随机生成问题
problems = []
for i in range(N):
    submit_num = randint(0, 1000)
    ac_num = randint(0, submit_num)
    problems.append(Problem(
        name=f'A+B问题@{i}',
        level=choice(levels),
        ac_num=ac_num,
        submit_num=submit_num,
        description="输入两个数字a和b，输出a+b",
        time_limit=randint(500, 5000),  # ms
        memory_limit=randint(10240, 102400),  # KB
    ))
Session.add_all(problems)

# 随机生成用户
users = []
ph = PasswordHasher()
Session.add(User(username='admin', password=ph.hash('1111111a'), email='admin@mail.com', is_admin=True))
Session.add(User(username='Nyan', password=ph.hash('1111111a'), email='aaa@aaa.com'))
Session.add(User(username='Tanix', password=ph.hash('1111111a'), email='tanix@tanix.com'))
usernames = {''.join(choices(string.ascii_letters + string.digits, k=randint(
    Config.USERNAME_MIN_LEN, Config.USERNAME_MAX_LEN
))) for _ in range(int(N * 1.1))}
email_suffix = '@mail.ustc.edu.cn'
emails = {''.join(choices(string.ascii_letters, k=randint(
    1, Config.EMAIL_MAX_LEN - len(email_suffix))
                          )) + email_suffix for _ in range(int(N * 1.1))}
for _ in range(N):
    users.append(User(
        username=usernames.pop(),
        password=ph.hash(''.join(choices(string.ascii_letters + string.digits, k=randint(
            Config.PWD_MIN_LEN, Config.PWD_MAX_LEN
        )))),
        email=emails.pop(),
        is_admin=choice([True, False])
    ))
Session.add_all(users)

# 提交了problem.id才不为None
Session.commit()

# 随机生成提交记录
submissions = []
for _ in range(N):
    problem = choice(problems)
    submissions.append(Submission(
        submission_time=datetime(randint(2000, 2021), randint(1, 12), randint(1, 28)),
        username=choice(users).username,
        problem_id=problem.id,
        compiler=choice(compilers),
        status=choice(stateses),
        time_cost=randint(0, problem.time_limit),  # ms
        memory_cost=randint(0, problem.memory_limit)  # KB
    ))
Session.add_all(submissions)

Session.commit()
