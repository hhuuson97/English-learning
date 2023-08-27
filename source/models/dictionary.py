import logging
import sqlalchemy as sa

from source.models.database import Base

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    word = sa.Column(sa.String(80), index=True)
    ipa = sa.Column(sa.String(80))
    mean = sa.Column(sa.String(255))
    has_voice = sa.Column(sa.Boolean)
