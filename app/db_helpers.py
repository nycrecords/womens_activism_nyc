"""
.. module:: db_helpers
	:synopsis: Functions that interact with the Postgres database via Flask-SQLAlchemy
.. modlueauthor:: Richa Agarwal <richa@codeforamerica.org>
"""
from app import db
from flask import current_app


def put_obj(obj):
    """
    Add and commit the object to the database. Return true if successful.
    """
    if obj:
        db.session.add(obj)
        db.session.commit()
        current_app.logger.info("\n\nCommitted object to database: %s" % obj)
        return True
    return False
