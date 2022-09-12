from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


def quick_table_count(table):
    pk = getattr(table, table.__mapper__.primary_key[0].name)
    return table.query.session.query(func.count(pk)).scalar()
