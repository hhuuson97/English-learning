import logging
import tempfile

from google.cloud import storage

from source.helpers import contants
from source.models.database import db_session
from source.models.dictionary import Dictionary

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)


def upload_from_file(bucket_name, file, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0
    blob.upload_from_file(file, if_generation_match=generation_match_precondition)
    file.seek(0)

def cache_voice_file(file, name):
    try:
        upload_from_file(contants.SETTINGS.BUCKET_ID, file, f"{name}.mp3")
        dict_info = Dictionary.query.filter(Dictionary.word == name).first()
        dict_info.has_voice = True
        db_session.commit()
    except Exception as e:
        _logger.error(e)

def get_voice_file(name):
    dict_info = Dictionary.query.filter(Dictionary.word == name).first()
    if dict_info.has_voice:
        try:
            return download_to_file(contants.SETTINGS.BUCKET_ID, f"{name}.mp3")
        except Exception as e:
            _logger.error(e)
    return None

def download_to_file(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    with tempfile.NamedTemporaryFile() as tmp:
        blob.download_to_file(file_obj=tmp)
        return tmp
