# coding=utf-8
import logging
import pytest
import os
from source.models.database import db_session, Base, init_db, init_engine, get_engine, DB_KEY_DEFAULT
from source.main_app import create_app, init_exts, init_api

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

os.environ['ENV_MODE'] = 'test'


@pytest.fixture(autouse=True, scope="session")
def app(request):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    init_engine("sqlite://", DB_KEY_DEFAULT)
    init_db(app)
    init_exts(app)
    init_api(app)
    Base.metadata.create_all(bind=get_engine())

    def teardown():
        db_session.close_all()
        db_session.remove()

        try:
            Base.metadata.drop_all(bind=get_engine())
        except Exception as e:
            print(e)

        ctx.pop()

    request.addfinalizer(teardown)

    return app
