'''
Utility functions used for view functions involving login
'''
from app.models import Events
from app.db_utils import create_object
from app.constants.event import LOGIN_FAILED, LOGIN_SUCCESS

def create_login_log(user, login_validation, emailAttempted=None):
    """
    A utility function to log login information (success and failure) in Events table
    :param user: the user attempting to login to the system (Users object)
    :param login_validation: a boolean that indicates if a login is a success or a fail
    """

    if login_validation:
        create_object(Events(
            _type=LOGIN_SUCCESS,
            user_guid=user.guid
        ))
    else:
        """
        the attempted login email will be stored in new_value column
        """
        tempGuid = None if user is None else user.guid
        create_object(Events(
            _type=LOGIN_FAILED,
            user_guid=tempGuid,
            new_value={'attempted_email': emailAttempted}
        ))
