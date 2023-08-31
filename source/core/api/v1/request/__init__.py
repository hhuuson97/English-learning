# coding=utf-8
import logging

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

from source.core.api import api
from .voice import VOICE_FILE_UPLOADER, GET_VOICE
from .library import UPSERT_WORD

HEADER_AUTH = api.parser()
HEADER_AUTH.add_argument('Authorization', location='headers', required=True)

HEADER_AUTH_OPTION = api.parser()
HEADER_AUTH_OPTION.add_argument('Authorization', location='headers', required=False)
