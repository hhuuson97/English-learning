# coding=utf-8
import logging
from source import app, celery

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app.run()
