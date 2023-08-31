import logging
import random
from typing import List
from flask import request
from sqlalchemy import func
from flask_login import current_user

from source.core import api
from source.core.api.v1 import web_v1_api
from source.models.dictionary import Dictionary
from source.models.user_exp import UserExp
from source.utils import languages
from source.utils.languages import load_word_info

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

class LibraryApi(api.v1.BaseResource, api.v1.BaseApi):

    @api.v1.login_required
    @web_v1_api.expect(api.v1.request.HEADER_AUTH, api.v1.request.library.GET_SAMPLE)
    def get(self):
        user_id = current_user.user_id
        excepted_word = request.args.get('excepted_word')
        MAX_RANDOM_LIST = 20
        # old mistake
        words: List[Dictionary] = Dictionary.query.filter(
            UserExp.query.filter(
                UserExp.user_id == user_id,
                UserExp.dict_id == Dictionary.id,
                UserExp.exactly_times <= 3,
            ).exists(),
            Dictionary.word != excepted_word,
        ).order_by(func.random()).limit(MAX_RANDOM_LIST).all()
        # new word
        if len(words) < MAX_RANDOM_LIST:
            more_words: List[Dictionary] = Dictionary.query.filter(
                ~UserExp.query.filter(
                    UserExp.user_id == user_id,
                    UserExp.dict_id == Dictionary.id,
                ).exists(),
                Dictionary.word != excepted_word,
            ).order_by(func.random()).limit(MAX_RANDOM_LIST - len(words)).all()
            words += more_words
        # review random
        if len(words) < MAX_RANDOM_LIST:
            more_words: List[Dictionary] = Dictionary.query.filter(
                Dictionary.word != excepted_word,
            ).order_by(func.random()).limit(MAX_RANDOM_LIST - len(words)).all()
            words += more_words

        chosen_word = words[int(random.random()*len(words))]
        if not chosen_word.mean:
            chosen_word = load_word_info(chosen_word.word)

        return self.return_general(200, message="ok", data={
            'word': chosen_word.word,
            'ipa': chosen_word.ipa,
            'mean': chosen_word.mean,
        })

    @api.v1.login_required
    @web_v1_api.expect(api.v1.request.HEADER_AUTH, api.v1.request.UPSERT_WORD)
    def post(self):
        word = request.json.get('word')
        languages.get_word_info(word)
        return self.return_general(200, message="ok")
