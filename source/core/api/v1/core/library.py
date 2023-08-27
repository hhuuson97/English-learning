import logging
import random
from typing import List

from flask import request
from sqlalchemy import func

from source.core import api
from source.models.dictionary import Dictionary
from source.models.user_exp import UserExp
from source.utils import languages

__author__ = 'son.hh'

from source.utils.languages import load_word_info

_logger = logging.getLogger(__name__)

class LibraryApi(api.v1.BaseResource, api.v1.BaseApi):

    def get(self):
        # Mock user_id
        user_id = '1'
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

    def post(self):
        word = request.json.get('word')
        languages.get_word_info(word)
        return self.return_general(200, message="ok")
