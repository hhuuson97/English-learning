import logging
import click
from flask.cli import with_appcontext

from source.models.database import db_session
from source.models.dictionary import Dictionary

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

@click.command()
@with_appcontext
def migrate_database():
    f = open("./migrations/data/en_UK.txt", "r")
    data = f.read()
    lines = data.split('\n')
    for line in lines:
        info = line.split('\t')
        if len(info) == 1:
            continue
        word = info[0]
        ipa = info[1]
        _logger.info(f'Insert {word} | {ipa}')
        db_session.add(Dictionary(word=word, ipa=ipa))
        db_session.flush()
    db_session.commit()
