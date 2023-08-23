import logging
import sqlalchemy as sa

from source.models.database import Base

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

class UserExp(Base):
    __tablename__ = 'user_exp'

    user_id = sa.Column(sa.String(36), primary_key=True)
    dict_id = sa.Column(sa.Integer, primary_key=True)
    exactly_times = sa.Column(sa.Integer)
