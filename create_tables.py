from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:731128@127.0.0.1:3306/ustcoj2022?charset=utf8"
db = SQLAlchemy(app)


class Problem(db.Model):
    __tablename__ = 'Problem'
    Problem_ID = db.Column(db.Integer,
                           nullable=False, primary_key=True)
    Problem_Title = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def to_model(cls, **kwargs):
        res = Problem()
        columns = [c.name for c in cls.__table__.columns]
        for k, v in kwargs.items():
            if k in columns:
                setattr(res, k, v)
        return res


db.drop_all()
db.create_all()

x = {'Problem_ID': '1001', 'Problem_Title': 'A+B问题'}
db.session.add(Problem.to_model(**x))

db.session.commit()
