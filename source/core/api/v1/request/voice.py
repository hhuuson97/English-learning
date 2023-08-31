import logging

from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

VOICE_FILE_UPLOADER = reqparse.RequestParser()
VOICE_FILE_UPLOADER.add_argument('url', type=str, location='form', help='Url để server tải về hoặc')
VOICE_FILE_UPLOADER.add_argument('file', type=FileStorage, location='files', help='File dạng binary')
VOICE_FILE_UPLOADER.add_argument('input', type=str, location='form', help='Kết quả dùng để kiểm tra')

GET_VOICE = reqparse.RequestParser()
GET_VOICE.add_argument('text', type=str, required=True, help="Từ cần lấy giọng nói")
