# coding=utf-8
import contextlib
import logging
import os
import functools
import flask_migrate
import click
from flask.cli import with_appcontext
from flask import current_app

from source.models.database import db_session, get_engine, init_db

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


@contextlib.contextmanager
def task_printing(msg):
    print(msg, '...', end=' ')
    yield
    print('done')


def init_task(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with task_printing('Start %s: %s, %s'
                           % (
                                   fn.__name__,
                                   args,
                                   kwargs,
                           )
                           ):
            fn(*args, **kwargs)

    return wrapper


@init_task
def _run_sql_file(file):
    if os.path.isfile(file):
        with open(file) as f:
            sql = f.read()
            get_engine().execute(sql)


@init_task
def init_users():
    _run_sql_file(os.path.join(current_app.config.get('SEEDS_DIR'), 'users.sql'))


@init_task
def import_file(file):
    _run_sql_file(os.path.join(current_app.config.get('SEEDS_DIR'), file))


@click.command()
@with_appcontext
def create_structure_db():
    """This command will initialize database, including:

    1. Create all tables
    2. Initialize areas table data with overwriting
    """
    # create all table
    with task_printing('Create database structure'):
        init_db(current_app, create=True)
        flask_migrate.stamp()
    # init areas table data
    init_users()

    db_session.commit()
