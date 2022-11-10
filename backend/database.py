from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase, MappedAsDataclass

from backend.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

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
