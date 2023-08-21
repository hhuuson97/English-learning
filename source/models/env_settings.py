# coding=utf-8
import logging
import sqlalchemy as sa
from .database import Base

_logger = logging.getLogger(__name__)


class EnvSettings(Base):

    __tablename__ = 'env_settings'

    name = sa.Column(sa.String(256), primary_key=True)
    value = sa.Column(sa.Text)
    group = sa.Column(sa.String(256))
    status = sa.Column(sa.Boolean, default=False)
    display_for_web = sa.Column(sa.Boolean, default=False)
