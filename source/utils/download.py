import logging
import io
from typing import Union
from werkzeug.datastructures import FileStorage
import urllib3

from source.helpers import contants, string_helpers, languages_helpers


__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

def download_file_from_server(url, max_content_size=None) -> (bool, Union[FileStorage, str]):
    """
    Download file from url
    :return:
    """
    if not url:
        return False, languages_helpers.get(contants.MESSAGES.MISSING_DATA), ""
    pool = urllib3.PoolManager()
    response = pool.urlopen('GET', url, preload_content=False, timeout=5)
    content_bytes = response.headers.get("Content-Length")
    if content_bytes and int(content_bytes) > max_content_size:
        response.release_conn()
        return False, languages_helpers.get(contants.MESSAGES.MAX_CONTENT_LENGTH_VALIDATE), ""
    file_name = url.split('/')[-1]
    if '.' not in file_name or file_name.split(".")[-1] == file_name:
        content_type = response.headers.get("Content-Type")
        if content_type and 'image' in content_type:
            file_name = str(string_helpers.md5(file_name)) + '.jpg'

    file_data = response.read()
    buffered = io.BytesIO(file_data)
    file = FileStorage(stream=buffered, filename=file_name, content_length=len(file_data))
    file.stream.flush()
    file.stream.seek(0)
    response.release_conn()
    if file.content_length > max_content_size:
        return False, languages_helpers.get(contants.MESSAGES.MAX_CONTENT_LENGTH_VALIDATE)
    return True, file
