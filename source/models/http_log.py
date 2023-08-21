import logging
from datetime import datetime
import json as _json
import sqlalchemy as db
from source.models.database import Base, db_session

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


class HttpLog(Base):
    __tablename__ = 'http_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text)
    header = db.Column(db.Text)
    method = db.Column(db.String(20))
    param = db.Column(db.Text)
    body = db.Column(db.Text)
    response = db.Column(db.Text)
    type = db.Column(db.String(50))
    user_agent = db.Column(db.String(400))
    client_ip = db.Column(db.String(50))
    uri_pattern = db.Column(db.String(255), index=True)

    user_id = db.Column(db.String(36), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self, response):
        try:
            self.response = _json.dumps(response) if response else None
            db_session.commit()
        except Exception as ex:
            _logger.error(ex)
