from backend.db import db
from backend.models import *


def add_data():
    db.session.add(Problem(ID='1001', Title='A+B问题@001'))
    db.session.add(Problem(ID='1002', Title='A+B问题@002'))
    db.session.add(Problem(ID='1003', Title='A+B问题@003'))
    db.session.add(Problem(ID='1004', Title='A+B问题@004'))
    db.session.add(Problem(ID='1005', Title='A+B问题@005'))
    db.session.add(Problem(ID='1006', Title='A+B问题@006'))
    db.session.add(Problem(ID='1007', Title='A+B问题@007'))
    db.session.add(Problem(ID='1008', Title='A+B问题@008'))
    db.session.add(Problem(ID='1009', Title='A+B问题@009'))
    db.session.add(Problem(ID='1010', Title='A+B问题@010'))
    db.session.add(Problem(ID='1011', Title='A+B问题@011'))
    db.session.add(Problem(ID='1012', Title='A+B问题@012'))
    db.session.add(Problem(ID='1013', Title='A+B问题@013'))
    db.session.add(Problem(ID='1014', Title='A+B问题@014'))
    db.session.add(Problem(ID='1015', Title='A+B问题@015'))
    db.session.add(Problem(ID='1016', Title='A+B问题@016'))
    db.session.add(Problem(ID='1017', Title='A+B问题@017'))
    db.session.add(Problem(ID='1018', Title='A+B问题@018'))
    db.session.commit()
