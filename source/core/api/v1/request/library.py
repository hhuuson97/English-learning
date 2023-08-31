import logging

from flask_restx import fields

from source.core.api import api

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

UPSERT_WORD = api.model(
    'UpsertWord', {
        'word': fields.String(required=True, description='Upsert new word'),
    }
)

GET_SAMPLE = api.model(
    'GetSample', {
        'excepted_word': fields.String(required=True, description='Get sample word from dictionary except this word')
    }
)