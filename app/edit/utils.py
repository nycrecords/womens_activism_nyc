"""
Utility functions used for view functions involving stories
"""
import uuid
from flask import current_app
from app.constants.user_type_auth import ANONYMOUS_USER
from app.constants.event import STORY_CREATED, USER_CREATED, EDIT_STORY, DELETE_STORY
from app.constants.flag import INCORRECT_INFORMATION
from app.models import Stories, Users, Events, Flags
from app.db_utils import edit_object, create_object

def hide_story(story_id):
    '''
    A utility function to hide/delete a Story object.
    :param story_id: the story_id you would like to hide
    :return: no return value
    '''
    story = Stories.query.filter_by(id=story_id).one()
    story.is_visible = False
    edit_object(story)

    # We should keep the same code for this one, since we need to create a new audit trail anyways in Events table for
    # hiding
    # Create Events object
    create_object(Events(
        _type=DELETE_STORY,
        story_id=story.id,
        new_value=story.val_for_events
    ))

    # Not sure what this is
    # Create the elasticsearch story doc
    if current_app.config['ELASTICSEARCH_ENABLED']:
        story.es_create()

    return story.id


def edit_story(story_id,
                activist_first,
                activist_last,
                activist_start,
                activist_end,
                tags,
                content,
                activist_url,
                image_url,
                video_url,
                user_guid,
                reason):
    """
    A utility function to edit a Story object and convert parameters to the correct data types. After the Story object
    is edited, it will be added and committed to the database

    :param story_id: the story_id you are editing
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
    :param reason: the reason for editing this post
    :return: no return value, a Story object will be created
    """
    strip_fields = ['activist_first', 'activist_last', 'activist_start', 'activist_end', 'content', 'activist_url',
                    'img_url', 'video_url']
    for field in strip_fields:
        field.strip()

    # convert "Today" to 9999 to be stored in the database
    if activist_end:
        activist_end = 9999 if activist_end.lower() == 'today' else int(activist_end)
    else:
        activist_end = None

    # Retrieving the story using story_id to edit
    story = Stories.query.filter_by(id=story_id).one()
    story.activist_first = activist_first.title()
    story.activist_last = activist_last.title()
    story.activist_start = int(activist_start) if activist_start else None
    story.activist_end = activist_end if activist_start and activist_last else None
    story.content = content
    story.activist_url = activist_url if activist_url else None
    story.image_url = image_url if image_url else None
    story.video_url = video_url if video_url else None
    story.user_guid = user_guid
    story.tags = tags
    story.is_edited = True

    # bring the Flags table here
    flag = Flags.query.filter_by(story_id=story_id).first()
    # if flag is None:
    flag = Flags(story_id=story_id,
                 type=INCORRECT_INFORMATION,
                 reason=reason)
    create_object(flag)
    # else:
    #     flag.type=flag.INCORRECT_INFORMATION
    #     flag.reason=reason
    #     edit_object(flag)

    edit_object(story)

    # We should keep the same code for this one, since we need to create a new audit trail anyways in Events table
    # Create Events object
    create_object(Events(
        _type=EDIT_STORY,
        story_id=story.id,
        new_value=story.val_for_events
    ))

    # Not sure what this is
    # Create the elasticsearch story doc
    if current_app.config['ELASTICSEARCH_ENABLED']:
        story.es_create()

    return story.id


def edit_user(story_id,
                user_first,
                user_last,
                user_email):
    """
    A utility function used to create a User object.
    If any of the fields are left blank then convert them to None types

    :param user_first: the poster's first name
    :param user_last: the poster's last name
    :param user_email: the poster's email
    :param user_email: the poster's password (default = None)
    :return: no return value, a Poster object will be created
    """
    strip_fields = ['user_first', 'user_last', 'user_email', 'password_hash']
    for field in strip_fields:
        field.strip()

    # Find out who the poster is from Stories (user_guid)
    story = Stories.query.filter_by(id=story_id).one()
    if story.user_guid is None:
        # create a new user if it didn't exist before
        user = Users(guid=str(uuid.uuid4()),
                     first_name=user_first if user_first else None,
                     last_name=user_last if user_last else None,
                     auth_user_type=ANONYMOUS_USER,
                     email=user_email if user_email else None,
                     password_hash=None)

        create_object(user)
        # Create Events object
        create_object(Events(
            _type=USER_CREATED,
            user_guid=user.guid,
            new_value=user.val_for_events
        ))


    else:
    # Find the difference and update them
        user = Users.query.filter_by(guid=story.user_guid).one()
        if user.first_name != user_first:
            user.first_name = user_first
        if user.last_name != user_last:
            user.last_name = user_last
        if user.email != user_email:
            user.email = user_email
        edit_object(user)
        create_object(Events(
            _type=USER_EDITED,
            user_guid=story.user_guid,
            new_value=user.val_for_events
        ))

    return user.guid
