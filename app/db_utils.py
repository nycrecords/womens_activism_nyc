"""
Utility functions used for database operations
"""

from app import db
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