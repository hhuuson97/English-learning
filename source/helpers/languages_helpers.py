# coding=utf-8
import logging
import os
from configparser import ConfigParser
from flask import request, has_app_context, has_request_context

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

LANGUAGE_OBJ = {}


def get(key, ):
    global LANGUAGE_OBJ
    default_lang = 'vi'
    lang = ''
    if has_app_context() and has_request_context() and 'Accept-Language' in request.headers:
        lang = request.headers['Accept-Language'].split(',')[0]
        if '-' in lang:
            lang = lang.split('-')[0]
    if lang not in LANGUAGE_OBJ:
        lang = default_lang

    if lang in LANGUAGE_OBJ and key in LANGUAGE_OBJ[lang]:
        return LANGUAGE_OBJ[lang][key]
    return ""


def init_languages(app):
    global LANGUAGE_OBJ
    current_path = os.path.join(app.config['ROOT_DIR'], 'source', 'languages')
    for file in os.listdir(current_path):
        if file.endswith(".ini"):
            try:
                config = ConfigParser()
                config.optionxform = str
                with open(os.path.join(current_path, file), encoding='utf-8') as stream:
                    config.read_string("[LANG]\n" + stream.read())
                name = os.path.splitext(os.path.basename(file))[0]
                LANGUAGE_OBJ[name] = {}
                for key in config['LANG']:
                    LANGUAGE_OBJ[name][key] = config['LANG'][key]
            except Exception as e:
                _logger.error("Read config language error: %s", str(e))
