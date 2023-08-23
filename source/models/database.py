# coding=utf-8
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

DB_KEY_DEFAULT = 'default'
DB_KEY_REPORTS = 'reports'
DB_KEYS = [DB_KEY_DEFAULT, DB_KEY_REPORTS]

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

engines = {
    DB_KEY_DEFAULT: None,
    DB_KEY_REPORTS: None
}

db_session = scoped_session(sessionmaker(
    # bind=engines[DB_KEY_DEFAULT, DB_KEY_REPORTS],
    autocommit=False,
    twophase=True  # if use multiple db
))
Base = declarative_base()
Base.query = db_session.query_property()

# For multiple database
Base_RP = declarative_base()
Base_RP.query = db_session.query_property()


def init_engine(uri, db_key, **kwargs):
    global engines
    if db_key == DB_KEY_DEFAULT:
        engines[DB_KEY_DEFAULT] = create_engine(uri, **kwargs)
        return engines[DB_KEY_DEFAULT]
    return None


def init_engine_all(config, **kwargs):
    global engines
    if config.get('SQLALCHEMY_DATABASE_BINDS'):
        for key, value in config.get('SQLALCHEMY_DATABASE_BINDS').items():
            engines[key] = create_engine(value, **kwargs)
    elif config.get('SQLALCHEMY_DATABASE_URI'):
        engines[DB_KEY_DEFAULT] = create_engine(config.get('SQLALCHEMY_DATABASE_URI'), **kwargs)
        engines[DB_KEY_REPORTS] = create_engine(config.get('SQLALCHEMY_DATABASE_URI'), **kwargs)


def get_engine(db=None):
    """
    Return base Engine
    :param db:
    :return: sqlalchemy.engine.Engine
    """
    global engines
    if db in engines:
        return engines[db]
    return engines[DB_KEY_DEFAULT]


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def init_db(app, db_key=None, create=None):
    global engines
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from source.models.env_settings import EnvSettings
    from source.models.user import User
    from source.models.http_log import HttpLog
    from source.models.dictionary import Dictionary
    # db_session.configure(
    #     bind=engines[db_key] if db_key in engines else engines[DB_KEY_DEFAULT]
    # )

    # For multiple database
    db_session.configure(
        binds={
            EnvSettings: engines[DB_KEY_DEFAULT],
            User: engines[DB_KEY_DEFAULT],
            HttpLog: engines[DB_KEY_DEFAULT],
            Dictionary: engines[DB_KEY_DEFAULT],
        }
    )

    if create:
        for engine in engines:
            if engine:
                Base.metadata.create_all(bind=engine)
