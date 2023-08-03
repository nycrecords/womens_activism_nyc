"""
Utility functions used for view functions involving stories
"""
import uuid

from flask import current_app, render_template, url_for

from app.constants.event_type import STORY_CREATED, USER_CREATED, NEW_SUBSCRIBER, UNSUBSCRIBED_EMAIL, UNSUBSCRIBED_PHONE
from app.constants.user_type_auth import ANONYMOUS_USER
from app.db_utils import create_object, update_object
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
    story = Stories(activist_first=activist_first,
                    activist_last=activist_last,
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
                user_email,
                user_phone):
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
    A utility function used to create a Subscriber object.
    If any of the fields are left blank then convert them to None types.
    Email admins and subscriber (if email is provided) notification of subscription.

    :param first_name: subscriber's first name
    :param last_name: subscriber's last name
    :param email: subscriber's email
    :param phone: subscriber's phone number
    """
    subscriber = Subscribers(first_name or None,
                             last_name or None,
                             email or None,
                             phone or None)

    create_object(subscriber)

    create_object(Events(
        _type=NEW_SUBSCRIBER,
        new_value={'subscriber_id': subscriber.id}
    ))

    # Email for the admin
    email_body = render_template('emails/new_subscriber_agency.html',
                                 first_name=first_name or 'Not Provided',
                                 last_name=first_name or 'Not Provided',
                                 email=email or 'Not Provided',
                                 phone=phone or 'Not Provided')
    send_email(subject="WomensActivism - New Subscriber",
               sender=current_app.config['MAIL_SENDER'],
               recipients=[current_app.config['MAIL_RECIPIENTS']],
               html_body=email_body)

    # Email for the user
    if email:
        unsubscribe_link = url_for('unsubscribe.unsubscribe', _external=True)
        email_user_body = render_template('emails/new_subscriber_user.html',
                                          first_name=first_name or 'Not Provided',
                                          last_name=last_name or 'Not Provided',
                                          unsubscribe_link=unsubscribe_link)
        send_email(subject="WomensActivism - Confirmation Email",
                   sender=current_app.config['MAIL_SENDER'],
                   recipients=[email],
                   html_body=email_user_body)


def remove_subscriber(email, phone):
    """
    A utility function used to create a Subscriber object.
    Clears database field for based on provided input field and value.

    :param email: email to be removed from subscriber's table
    :param phone: email to be removed from subscriber's table
    """
    if email:
        email_subscribers = Subscribers.query.filter_by(email=email).all()
        for s in email_subscribers:
            update_object({"email": None}, Subscribers, s.id)

            create_object(Events(
                _type=UNSUBSCRIBED_EMAIL,
                new_value={'subscriber_id': s.id}
            ))

    if phone:
        phone_subscribers = Subscribers.query.filter_by(phone=phone).all()
        for s in phone_subscribers:
            update_object({"phone": None}, Subscribers, s.id)
            create_object(Events(
                _type=UNSUBSCRIBED_PHONE,
                new_value={'subscriber_id': s.id}
            ))
