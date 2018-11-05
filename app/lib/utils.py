"""
Utility functions used for view functions involving stories
"""
import uuid

from flask import current_app, render_template
from sqlalchemy import or_

from app.constants.event_type import STORY_CREATED, USER_CREATED, NEW_SUBSCRIBER
from app.constants.user_type_auth import ANONYMOUS_USER
from app.db_utils import create_object, bulk_delete
from app.lib.emails_utils import send_email
from app.models import Stories, Users, Events, Subscribers


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
        activist_end = 9999 if activist_end.lower() == 'today' else int(activist_end)
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
        user_guid=user_guid,
        new_value=story.val_for_events
    ))

    # Create the elasticsearch story doc
    if current_app.config['ELASTICSEARCH_ENABLED']:
        story.es_create()

    return story.id


def create_user(user_first,
                user_last,
                user_email=None,
                user_phone=None):
    """
    A utility function used to create a User object.
    If any of the fields are left blank then convert them to None types

    :param user_first: the poster's first name
    :param user_last: the poster's last name
    :param user_email: the poster's email
    :param user_phone: the poster's phone
    :return: no return value, a User object will be created
    """
    strip_fields = ['user_first', 'user_last', 'user_email']
    for field in strip_fields:
        field.strip()

    # Create Users object
    user = Users(guid=str(uuid.uuid4()),
                 first_name=user_first if user_first else None,
                 last_name=user_last if user_last else None,
                 auth_user_type=ANONYMOUS_USER,
                 email=user_email,
                 phone=user_phone)
    create_object(user)

    # Create Events object
    create_object(Events(
        _type=USER_CREATED,
        user_guid=user.guid,
        new_value=user.val_for_events
    ))
    return user.guid


def create_subscriber(first_name,
                      last_name,
                      email,
                      phone):
    """

    :param first_name:
    :param last_name:
    :param email:
    :param phone:
    :return:
    """
    subscriber = Subscribers(first_name or None,
                             last_name or None,
                             email or None,
                             phone or None)

    create_object(subscriber)

    create_object(Events(
        _type=NEW_SUBSCRIBER,
        new_value=subscriber.id
    ))


def remove_subscriber(email, phone):
    """

    :param email:
    :param phone:
    :return:
    """
    query = Subscribers.query.filter(or_(Subscribers.email == email, Subscribers.phone == phone))

    bulk_delete(query)

    # TODO: Send email to admins
    # email_body = render_template('emails/remove_subscriber_agency.html',
    #                              first_name=user.first_name,
    #                              last_name=user.last_name,
    #                              email=form.user_email.data,
    #                              phone=user.phone)
    # send_email(subject="WomensActivism - Remove Subscriber",
    #            sender=current_app.config['MAIL_SENDER'],
    #            recipients=[current_app.config['MAIL_RECIPIENTS']],
    #            html_body=email_body)
    # create_object(Events(
    #     _type=EMAIL_SENT,
    #     user_guid=user_guid,
    #     new_value={"email_body": email_body}))
