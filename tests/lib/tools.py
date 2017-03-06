import random
from itertools import product

from string import (
    ascii_lowercase,
    digits
)

from tests.lib.constants import (
    NON_ANON_USER_GUID_LEN,
)

from app import db
from app.constants import tag, user_type_auth
from app.lib.db_utils import create_object
from app.models import Stories, Users
from app.share.utils import generate_guid


def create_stories_search_set():
    for activist_first, activist_last, content in product(("foo", "bar", "qux"), repeat=3):
        story = Stories(
            activist_first=activist_first,
            activist_last=activist_last,
            activist_start=1917,
            activist_end=1920,
            content=content,
            tags=[random.choice(tag.tags)],
        )
        db.session.add(story)
        db.session.commit()


def create_user(auth_type=user_type_auth.PUBLIC_USER_NYC_ID):
    """
    :param auth_type: one of app.constants.user_type_auth
    """
    len_firstname = random.randrange(3, 8)
    len_lastname = random.randrange(3, 15)
    firstname = ''.join(random.choice(ascii_lowercase)
                        for _ in range(len_firstname)).title()
    lastname = ''.join(random.choice(ascii_lowercase)
                       for _ in range(len_lastname)).title()
    user = Users(
        guid=generate_user_guid(auth_type),
        auth_user_type=auth_type,
        email='{}{}@email.com'.format(firstname[0].lower(), lastname.lower()),
        email_validated=True,
        terms_of_use_accepted=True)
    create_object(user)
    return user


def generate_user_guid(auth_type):
    """
    Generate a user guid based on the provided auth_type.
    """
    if auth_type == user_type_auth.ANONYMOUS_USER:
        return generate_guid()
    else:
        return ''.join(random.choice(ascii_lowercase + digits)
                       for _ in range(NON_ANON_USER_GUID_LEN))
