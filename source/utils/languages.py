import logging
from io import BytesIO
from typing import List, Union

import ffmpeg
import whisper
import numpy as np
import re
from googletrans.models import Translated
from gtts import gTTS
from googletrans import Translator
from werkzeug.datastructures import FileStorage

from source.models.database import db_session
from source.models.dictionary import Dictionary

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

lang_model = whisper.load_model("base")
translator = Translator()

SAMPLE_RATE = 16000

def load_audio(file_bytes: bytes, sr: int = SAMPLE_RATE) -> np.ndarray:
    """
    Use file's bytes and transform to mono waveform, resampling as necessary
    Parameters
    ----------
    file: bytes
        The bytes of the audio file
    sr: int
        The sample rate to resample the audio if necessary
    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input('pipe:', threads=0)
            .output("pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run_async(pipe_stdin=True, pipe_stdout=True)
        ).communicate(input=file_bytes)

    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

def speech_to_text(file: FileStorage):
    audio = load_audio(file.stream.read())
    result = lang_model.transcribe(audio, language="en")
    return result["text"]

def replace_un_word(text):
    return re.sub(r"[^a-zA-Z0-9\s]+", ".", text, 0, re.MULTILINE)

def text_to_speech(text: str):
    tts = gTTS(replace_un_word(text), lang="en", tld="com")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

def word_split(text: str) -> List[List[Union[int, str]]]:
    matches = re.finditer(r"\w+", text, re.MULTILINE)
    ret = []
    for matchNum, match in enumerate(matches, start=1):
        ret.append([match.start(), match.end(), match.group()])
    return ret

def load_word_info(text: str):
    dict_info = None
    try:
        k: Translated = translator.translate(text, dest='vi', src='en')
        dict_info = Dictionary.query.filter(Dictionary.word == text).first()
        if not dict_info:
            dict_info = Dictionary(word=text, ipa=k.pronunciation, mean=k.text)
            db_session.add(dict_info)
            db_session.commit()
        else:
            if k.pronunciation:
                dict_info.ipa = k.pronunciation
            if k.text:
                dict_info.mean = k.text
            db_session.flush()
    except Exception as e:
        _logger.error(e)
    return dict_info

def get_word_info(text: str):
    dict_info = Dictionary.query.filter(Dictionary.word == text).first()
    if not dict_info:
        dict_info = load_word_info(text)
    return dict_info
