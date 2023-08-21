import logging
from typing import List, Union

import whisper
import re
from gtts import gTTS

from werkzeug.datastructures import FileStorage

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

lang_model = whisper.load_model("tiny")

def speech_to_text(file: FileStorage):
    file.save("data.mp3")
    result = lang_model.transcribe("data.mp3", language="en")
    return result["text"]

def replace_un_word(text):
    return re.sub(r"[^a-zA-Z0-9\s]+", ".", text, 0, re.MULTILINE)

def text_to_speech(text: str):
    tts = gTTS(replace_un_word(text))
    return tts

def word_split(text: str) -> List[List[Union[int, str]]]:
    matches = re.finditer(r"\w+", text, re.MULTILINE)
    ret = []
    for matchNum, match in enumerate(matches, start=1):
        ret.append([match.start(), match.end(), match.group()])
    return ret
