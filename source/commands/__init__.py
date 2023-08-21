import logging

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

def init_cmds(app):
    from .init_db import create_structure_db

    app.cli.add_command(create_structure_db, 'init_db')
