"""
Utility functions used for view functions involving stories
"""
import uuid
from flask import current_app

from app.constants.user_type_auth import ANONYMOUS_USER
from app.constants.event import STORY_CREATED, USER_CREATED
from app.models import Stories, Users, Events
from app.db_utils import create_object


def create_story(activist_first,
                 activist_last,
                 activist_start,
                 activist_end,
                 tags,
                 content,
                 activist_url,
                 image_url,
                 video_url,
                 user_guid):
    """
    A utility function to create a Story object and convert parameters to the correct data types. After the Story object
    is created it will be added and committed to the database

    :param activist_first: the activist's first name
    :param activist_last: the activist's last name
    :param activist_start: the activist's birth year
    :param activist_end: the activist's death year
    :param tags: a string array containing the selected tags associated with the activist
    :param content: the content of the story
    :param activist_url: a url containing additional information about the activist
    :param image_url: a url containing an image link
    :param video_url: a url containing a
    :param user_guid: the guid of the user who created the story
    :return: no return value, a Story object will be created
    """
    strip_fields = ['activist_first', 'activist_last', 'activist_start', 'activist_end', 'content', 'activist_url',
                    'img_url', 'video_url']
    for field in strip_fields:
        field.strip()

    # convert "Today" to 9999 to be stored in the database
    if activist_end:
        activist_end = 9999 if (activist_end == 'Today' or activist_end == 'today') else int(activist_end)
    else:
        activist_end = None

    # Create Stories object
    story = Stories(activist_first=activist_first.title(),
                    activist_last=activist_last.title(),
                    activist_start=int(activist_start) if activist_start else None,
                    activist_end=activist_end,
                    content=content,
                    activist_url=activist_url if activist_url else None,
                    image_url=image_url if image_url else None,
                    video_url=video_url if video_url else None,
                    user_guid=user_guid,
                    tags=tags)
    create_object(story)

    # Create Events object
    create_object(Events(
        _type=STORY_CREATED,
        story_id=story.id,
        new_value=story.val_for_events
    ))

    # Create the elasticsearch story doc
    if current_app.config['ELASTICSEARCH_ENABLED']:
        story.es_create()


def create_user(user_first,
                user_last,
                user_email):
    """
    A utility function used to create a User object.
    If any of the fields are left blank then convert them to None types

    :param user_first: the poster's first name
    :param user_last: the poster's last name
    :param user_email: the poster's email
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
                 email=user_email if user_email else None)
    create_object(user)

    # Create Events object
    create_object(Events(
        _type=USER_CREATED,
        user_guid=user.guid,
        new_value=user.val_for_events
    ))

    return user.guid
