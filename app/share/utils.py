"""
Utility functions used for view functions involving stories
"""

from app.models import Stories, Users
from app.db_utils import create_object


def create_story(activist_first,
                 activist_last,
                 activist_start,
                 activist_start_BC,
                 activist_end,
                 activist_end_BC,
                 tags,
                 content,
                 activist_url,
                 image_url,
                 video_url,
                 user_id):
    """
    A utility function to create a Story object and convert parameters to the correct data types. After the Story object
    is created it will be added and committed to the database

    :param activist_first: the activist's first name
    :param activist_last: the activist's last name
    :param activist_start: the activist's birth year
    :param activist_start_BC:
    :param activist_end: the activist's death year
    :param activist_end_BC:
    :param tags: a string array containing the selected tags associated with the activist
    :param content: the content of the story
    :param activist_url:
    :param image_url: a url containing an image link
    :param video_url: a url containing a
    :param poster_id: the id of the poster who created the story
    :return: no return value, a Story object will be created
    """
    activist_first.strip()
    activist_first.title()
    activist_last.strip()
    activist_last.title()
    activist_start.strip()
    activist_end.strip()
    content.strip()
    activist_url.strip()
    image_url.strip()
    video_url.strip()

    if activist_start_BC:  # convert the year to a negative integer if the start year was in BC
        activist_start = int(activist_start) * -1
    if activist_end_BC:  # convert the year to a negative integer if the end year was in BC
        activist_end = int(activist_end) * -1
    if activist_end == "Today" or activist_end == "today":  # convert "Today" to 9999 to be stored in the database
        activist_end = 9999
    if activist_url == "":
        activist_url = None
    if image_url == "":
        image_url = None
    if video_url == "":
        video_url = None

    story = Stories(activist_first=activist_first,
                    activist_last=activist_last,
                    activist_start=activist_start,
                    activist_end=activist_end,
                    content=content,
                    activist_url=activist_url,
                    image_url=image_url,
                    video_url=video_url,
                    poster_id=poster_id,
                    tags=tags)

    create_object(story)


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
    user_first.strip()
    user_first.title()
    user_last.strip()
    user_last.title()
    user_email.strip()

    if user_first == "":
        user_first = None
    if user_last == "":
        user_last = None
    if user_email == "":
        user_email = None

    user = Users(first_name=user_first,
                 last_name=user_last,
                 email=user_email)

    create_object(user)
    return user.id
