import uuid
from flask import current_app

from app.constants.user_type_auth import ANONYMOUS_USER
from app.constants.event import USER_CREATED
from app.models import Users, Events
from app.db_utils import create_object

def create_user(user_first,
                user_last,
                user_email,
                user_phone):
    """
    A utility function used to create a User object.
    If any of the fields are left blank then convert them to None types

    :param user_first: the subscribers first name
    :param user_last: the subscribers  last name
    :param user_email: the subscribers email
    :param user_phone: the subscribers phone number
    :return: no return value, a Poster object will be created
    """
    strip_fields = ['user_first', 'user_last', 'user_email']
    for field in strip_fields:
        field.strip()

    # Create Users object
    user = Users(guid=str(uuid.uuid4()),
                 first_name=user_first if user_first else None,
                 last_name=user_last if user_last else None,
                 auth_user_type=ANONYMOUS_USER,
                 email=user_email if user_email else None,
                 phone=user_phone if user_phone else None
                 )
    create_object(user)

    # Create Events object
    create_object(Events(
        _type=USER_CREATED,
        user_guid=user.guid,
        new_value=user.val_for_events
    ))

    return user.guid