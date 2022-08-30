from backend.models import *


def add_data():
    db.session.add(Problem(ID=1001, Title='A+B问题@001',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1002, Title='A+B问题@002',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1003, Title='A+B问题@003',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1004, Title='A+B问题@004',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1005, Title='A+B问题@005',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1006, Title='A+B问题@006',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1007, Title='A+B问题@007',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1008, Title='A+B问题@008',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1009, Title='A+B问题@009',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1010, Title='A+B问题@010',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1011, Title='A+B问题@011',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1012, Title='A+B问题@012',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1013, Title='A+B问题@013',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1014, Title='A+B问题@014',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1015, Title='A+B问题@015',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1016, Title='A+B问题@016',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1017, Title='A+B问题@017',
                   Level='Easy', ac_num=2, submit_num=10))
    db.session.add(Problem(ID=1018, Title='A+B问题@018',
                   Level='Easy', ac_num=2, submit_num=10))

    db.session.add(User(username='Nyan_the_cat',
                   password='123456', email='aaa@aaa.com'))
    db.session.commit()

    db.session.add(Status(
        **{
            'submitTime': "2022-3-1",
            'problemId': "1001",
            'coder': "Nyan_the_cat",
            'status': "Accepted",
            'timeCost': "10",
            'memoryCost': "30"
        }
    ))

    db.session.add(Status(
        **{
            'submitTime': "2022-3-1",
            'problemId': "1002",
            'coder': "Nyan_the_cat",
            'status': "Compile Error",
            'timeCost': None,
            'memoryCost': None
        }
    ))

    db.session.commit()
