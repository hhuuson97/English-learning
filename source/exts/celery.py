# coding=utf-8
import logging
import celery as _celery
from celery.schedules import crontab
import kombu.serialization
from source.utils.cipher import json_encode, json_decode

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

kombu.serialization.register(
    name='app-json',
    encoder=json_encode,
    decoder=json_decode,
    content_type='application/app-json',
    content_encoding='utf-8'
)


def make_celery(app):
    """ Create a celery application from Flask application

    :param flask.Flask app: Flask application
    :return:
    :rtype: celery.Celery
    """
    celery = _celery.Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],

    )
    celery.conf.update(app.config)
    celery.conf.update(
        CELERY_TASK_SERIALIZER='app-json',
        CELERY_ACCEPT_CONTENT=['app-json', ],
        CELERY_RESULT_SERIALIZER='app-json',
    )

    # Nếu celery chạy async thì mới thêm appContext
    if not celery.conf.task_always_eager:
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask

    @celery.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        pass

    return celery
