"""
Utility functions used for view functions involving stories
"""
from flask_login import current_user
from flask import current_app

from app.constants.user_type_auth import ANONYMOUS_USER
from app.constants.event_type import EDIT_STORY, DELETE_STORY, USER_EDITED
from app.constants.flag import INCORRECT_INFORMATION
from app.db_utils import update_object, create_object
from app.models import Stories, Users, Events, Flags
from app.search.utils import delete_doc
import uuid

from tempfile import NamedTemporaryFile
from flask import current_app
from werkzeug.utils import secure_filename
from app import s3
import subprocess

def hide_story(story_id):
    """
    A utility function to hide/delete a Story object.

    :param story_id: the story_id you would like to hide
    :return: no return value
    """
    story = Stories.query.filter_by(id=story_id).one()

    old_json_value = {"is_visible": story.is_visible}

    story.is_visible = False
    new_json_value = {"is_visible": False}

    update_object(new_json_value, Stories, story.id)
    delete_doc(story.id)

    # We should keep the same code for this one, since we need to create a new audit trail anyways in Events table for
    # hiding
    # Create Events object
    create_object(Events(
        _type=DELETE_STORY,
        story_id=story.id,
        user_guid=current_user.guid,
        previous_value=old_json_value,
        new_value=new_json_value
    ))

    return story.id


def update_story(story_id,
                 activist_first,
                 activist_last,
                 activist_start,
                 activist_end,
                 tags,
                 content,
                 activist_url,
                 image_url,
                 image_pc,
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
    :param image_pc: a picture from the users pc
    :param video_url: a url containing a
    :param user_guid: the guid of the user who created the story
    :param reason: the reason for editing this post
    :return: no return value, a Story object will be created
    """
    strip_fields = ['activist_first', 'activist_last', 'activist_start', 'activist_end', 'content', 'activist_url',
                    'img_url','img_pc', 'video_url']
    for field in strip_fields:
        field.strip()

    # convert "Today" to 9999 to be stored in the database
    if activist_end:
        activist_end = 9999 if activist_end.lower() == 'today' else int(activist_end)
    else:
        activist_end = None

    # Retrieving the story using story_id to edit
    story = Stories.query.filter_by(id=story_id).one()

    story_fields = {
        "activist_first",
        "activist_last",
        "activist_start",
        "activist_end",
        "content",
        "activist_url",
        "image_url",
        "image_pc",
        "video_url",
        "user_guid",
        "tags"
    }

    story_field_vals = {
        "activist_first": activist_first,
        "activist_last": activist_last,
        "activist_start": int(activist_start) if activist_start else None,
        "activist_end": activist_end,
        "content": content,
        "activist_url": activist_url,
        "image_url": image_url,
        "image_pc": image_pc,
        "video_url": video_url,
        "user_guid": user_guid,
        "tags": tags
    }

    old = {}
    new = {}

    for field in story_fields:
        val = story_field_vals[field]
        if val is not None:
            if val == '':
                story_field_vals[field] = None  # null in db, not empty string
            cur_val = getattr(story, field)
            new_val = story_field_vals[field]
            if cur_val != new_val:
                old[field] = cur_val
                new[field] = new_val

    if new:
        story.is_edited = True
        update_object(new, Stories, story.id)

        create_object(Events(
            _type=EDIT_STORY,
            story_id=story.id,
            user_guid=current_user.guid,
            previous_value=old,
            new_value=new
        ))

        # bring the Flags table here
        flag = Flags(story_id=story_id,
                     type=INCORRECT_INFORMATION,
                     reason=reason)
        create_object(flag)

    return story.id


def update_user(user,
                first_name,
                last_name):
    """
    A utility function used to create a User object.
    If any of the fields are left blank then convert them to None types

    :param user: the user that will be updated
    :param first_name: the new updated version of poster's first name
    :param last_name: the new updated version of poster's last name

    :return: no return value, a Poster object will be created
    """
    user_fields = {
        'first_name',
        'last_name'
    }

    user_field_vals = {
        'first_name': first_name,
        'last_name': last_name
    }

    old = {}
    new = {}

    for field in user_fields:
        val = user_field_vals[field]
        if val is not None:
            if val == '':
                user_field_vals[field] = None  # null in db, not empty string
            cur_val = getattr(user, field)
            new_val = user_field_vals[field]
            if cur_val != new_val:
                old[field] = cur_val
                new[field] = new_val

    if new:
        update_object(new, user, user.guid)

        # Create Events object
        create_object(Events(
            _type=USER_EDITED,
            user_guid=current_user.guid,
            new_value={"user_guid": user.guid}
        ))

    return user.guid

def handle_upload(file_field):
    path = upload(file_field.data)
    return path


def upload(image_pc):
    # generates unique id for filename so nothing gets overwritten.
    image_pc.filename = str(uuid.uuid4())
    with NamedTemporaryFile(
        dir=current_app.config["UPLOAD_QUARANTINE_DIRECTORY"],
        suffix=".{}".format(secure_filename(image_pc.filename)),
        delete=False,
    ) as fp:
        image_pc.save(fp)
        data = open(fp.name, "rb")
        fp.name = fp.name.split(".", 1)[1]
        s3.Bucket("nycrecords-wom-uploads-dev").put_object(
            Key=fp.name, Body=data, ACL="public-read", ContentType="image/jpeg"
        )
        subprocess.call(["rm", "-rf", fp.name])
        return fp.name

