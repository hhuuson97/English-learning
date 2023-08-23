import logging

from source.models.database import db_session
from source.models.dictionary import Dictionary
from source.models.user_exp import UserExp

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

def add_more_exp(user_id, words, is_success):
    for word in words:
        dict_id = Dictionary.query.filter(Dictionary.word == word).first()
        if not dict_id:
            continue
        user_exp: UserExp = UserExp.query.filter(
            UserExp.user_id == user_id,
            UserExp.dict_id == dict_id,
        ).first()
        if user_exp:
            if is_success:
                user_exp.exactly_times += 1
            else:
                user_exp.exactly_times = 0
        else:
            user_exp = UserExp(
                user_id=user_id,
                dict_id=dict_id,
                exactly_times=1 if is_success else 0,
            )
            db_session.add(user_exp)
        db_session.flush()
    db_session.commit()
