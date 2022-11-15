from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase, MappedAsDataclass
from sqlalchemy.sql import Executable
from sqlalchemy.engine.result import ChunkedIteratorResult

from backend.config import Config

# echo设为True可以 debug sqlalechemy
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

try:
    from greenlet import getcurrent as _get_ident
except ImportError:
    from threading import get_ident as _get_ident

Session = scoped_session(sessionmaker(engine), scopefunc=_get_ident)

class Base(DeclarativeBase, MappedAsDataclass):
    pass

def init_app(app):
    @app.teardown_appcontext
    def remove_session(_exception):
        Session.remove()

def get_dicts(stmt: Executable):
    res = Session.execute(stmt)
    assert isinstance(res, ChunkedIteratorResult), 'type of r is not ChunkedIteratorResult'
    rows = res.raw.all()
    return [dict(row._mapping) for row in rows]  # noqa
