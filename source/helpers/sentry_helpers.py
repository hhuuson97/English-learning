# coding=utf-8
import logging
import traceback
import urllib.parse
import os
from sentry_sdk import capture_exception
from .http_request import HttpRequest
from flask import current_app, has_app_context

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def get_env():
    env_mode = os.environ.get('ENV_MODE', 'DEV').upper()
    if has_app_context():
        env_mode = current_app.config.get('ENV_MODE')
    return env_mode


def send_error_to_sentry(e, message=None, traceback=True):
    env_mode = get_env()
    return
    if env_mode != "DEV":
        try:
            capture_exception(e)
        except:
            pass
        try:
            send_telegram(e)
        except:
            pass

    if message:
        _logger.error(message)
    if traceback:
        _logger.exception(e)


def send_telegram(e, message=None):
    token = ""
    chat_id = 0
    env_mode = get_env()
    if env_mode == "DEV":
        return
    try:
        message = traceback.format_exc()
        message = "ENV: %s \n %s" % (env_mode, message)
        message = urllib.parse.quote(message)
        uri = "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}".format(
            token=token, chat_id=chat_id, message=message
        )
        HttpRequest.get(uri, is_log=False, timeout=2)
    except:
        pass
