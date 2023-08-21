# coding=utf-8
import logging
from . import main_app
from source.exts import celery as _celery

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

app = main_app.create_app()
celery = _celery.make_celery(app)

main_app.init_app(app)
