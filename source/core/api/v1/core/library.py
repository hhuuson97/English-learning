import logging
import random
from typing import List

from sqlalchemy import exists, or_, func

from source.core import api
from source.models.dictionary import Dictionary
from source.models.user_exp import UserExp

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

class LibraryApi(api.v1.BaseResource, api.v1.BaseApi):

    def get(self):
        # Mock user_id
        user_id = '1'
        MAX_RANDOM_LIST = 20
        # old mistake
        words: List[Dictionary] = Dictionary.query.filter(
            UserExp.query.filter(
                UserExp.user_id == user_id,
                UserExp.dict_id == Dictionary.id,
                UserExp.exactly_times <= 3,
            ).exists(),
        ).order_by(func.random()).limit(MAX_RANDOM_LIST).all()
        # new word
        if len(words) < MAX_RANDOM_LIST:
            more_words: List[Dictionary] = Dictionary.query.filter(
                ~UserExp.query.filter(
                    UserExp.user_id == user_id,
                    UserExp.dict_id == Dictionary.id,
                ).exists(),
            ).order_by(func.random()).limit(MAX_RANDOM_LIST - len(words)).all()
            words += more_words
        # review random
        if len(words) < MAX_RANDOM_LIST:
            more_words: List[Dictionary] = Dictionary.query.order_by(func.random()).limit(MAX_RANDOM_LIST - len(words)).all()
            words += more_words

        chosen_word = words[int(random.random()*len(words))]

        return self.return_general(200, message="ok", data={
            'word': chosen_word.word,
            'ipa': chosen_word.ipa,
            'mean': chosen_word.mean,
        })
