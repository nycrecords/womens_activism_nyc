'''
Utility functions used for view functions involving login
'''

from app.models import Users, Events
from app.db_utils import create_object
from app.constants.event import LOGIN_FAILED, LOGIN_SUCCESS

def create_login_log(user, login_validation):
    '''
    A utility function to log login success and failure in Events table
    :param form.data
    '''
    if login_validation:
        if user is not None:
            create_object(Events(
                _type=LOGIN_SUCCESS,
                user_guid=user.guid
            ))
    else:
        tempGuid = None if user is None else user.guid
        create_object(Events(
            _type=LOGIN_FAILED,
            user_guid=tempGuid
        ))
