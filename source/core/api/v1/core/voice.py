import logging
from io import BytesIO

from flask import request, send_file
from werkzeug.datastructures import FileStorage

from source.core import api
from source.core.api.v1 import web_v1_api
from source.utils import download, languages, algorithm

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

class VoiceApi(api.v1.BaseResource, api.v1.BaseApi):

    @web_v1_api.expect(api.v1.request.voice.GET_VOICE)
    def get(self):
        text = request.args.get('text')
        file = languages.text_to_speech(text)
        fp = BytesIO()
        file.write_to_fp(fp)
        fp.seek(0)
        return send_file(fp, download_name="data.mp3")

    @web_v1_api.expect(api.v1.request.voice.VOICE_FILE_UPLOADER)
    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files and 'url' not in request.form:
            return self.return_general(400, "No file")
        file = request.files.get('file') or request.form.get('url')
        input = request.form.get('input')
        # if user does not select file, browser also
        # submit an empty part without filename
        if not file or (isinstance(file, FileStorage) and file.filename == ''):
            return self.return_general(400, "No file")

        if not isinstance(file, FileStorage):
            success, file = download.download_file_from_server(file)
            if not success:
                return self.return_general(400, file)

        input2 = languages.speech_to_text(file)

        # Highlight the wrong words
        un_matches = algorithm.longest_common_words(languages.word_split(input), languages.word_split(input2))
        result = input
        for s, e, w in un_matches[::-1]:
            result = f"{result[:s]}<span class='wrongWord'>{w}</span>{result[e:]}"
        result = f"<p class='rightWord'>{result}</p>"

        return self.return_general(200, message="ok", data={'predict': input2, 'result': result})
