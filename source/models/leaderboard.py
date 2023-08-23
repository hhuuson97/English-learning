import logging
import sqlalchemy as sa

from source.models.database import Base

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

class LeaderBoard(Base):
    __tablename__ = 'leader_board'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.String(36))
    max_point = sa.Column(sa.Integer)
    game_type = sa.Column(sa.Integer)
