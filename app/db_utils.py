"""
Utility functions used for database operations
"""
from flask import current_app

from app import db
from app.models import Stories
import sys


def create_object(obj):
    """
    A utility function to add objects to the database

    :param obj: the object that is being added to the database
    :return: no return value, an object will be added to the database
    """
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        print("Failed to CREATE {} : {}".format(obj, e))
        print(sys.exc_info())
        db.session.rollback()
    else:
        # create elasticsearch doc
        if (not isinstance(obj, Stories)
            and hasattr(obj, 'es_create')
            and current_app.config['ELASTICSEARCH_ENABLED']):
              obj.es_create()
        return str(obj)


def edit_object(obj):
    try:
        db.session.commit()
    except Exception as e:
        print("Failed to EDIT {} : {}".format(obj, e))
        print(sys.exc_info())
        db.session.rollback()
    else:
        # create elasticsearch doc
        if (not isinstance(obj, Stories)
            and hasattr(obj, 'es_create')
            and current_app.config['ELASTICSEARCH_ENABLED']):
              obj.es_create()
        return str(obj)
