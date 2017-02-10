"""
Utility functions used for view functions involving stories
"""

from app.models import Stories, Posters
from app.db_utils import create_object


def validate_poster(poster_first, poster_last):
    """
    A validator used check that a poster has provided both their first and last name if they decide to give their personal
    information

    :param poster_first: the poster's first name
    :param poster_last: the poster's last name
    :return: True is validation is passed, False otherwise
    """
    if (len(poster_first) == 0 and len(poster_last) != 0) or (len(poster_first) != 0 and len(poster_last) == 0):
        return False
    else:
        return True


def validate_years(activist_start, activist_start_BC, activist_end, activist_end_BC):
    """
    A validator used to to check edge cases for activist years involving both the start and end years

    :param activist_start: the activist's birth year
    :param activist_start_BC: a boolean to see if the birth year was a BC year
    :param activist_end: the activist's death year
    :param activist_end_BC: a boolean to see if the death year was a BC year
    :return: True is the years are valid, False otherwise
    """
    if activist_end == "Today" and activist_end_BC:  # ensures "Today" and BC are not inputted at the same time
        return False

    # if the activist years are BC years then convert them to negative integers
    if activist_start_BC:
        activist_start = int(activist_start) * -1
    if activist_end_BC:
        activist_end = int(activist_end) * -1

    if activist_start > activist_end:
        return False
    return True


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
                 poster_id):
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
    if activist_start_BC:  # convert the year to a negative integer if the start year was in BC
        activist_start = int(activist_start) * -1
    if activist_end_BC:  # convert the year to a negative integer if the end year was in BC
        activist_end = int(activist_end) * -1
    if activist_end == "Today":  # convert "Today" to 9999 to be stored in the database
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


def create_poster(poster_first,
                  poster_last,
                  poster_email):
    """
    A utility function used to create a Poster object. If any of the fields are left blank then convert them to None types

    :param poster_first: the poster's first name
    :param poster_last: the poster's last name
    :param poster_email: the poster's email
    :return: no return value, a Poster object will be created
    """
    if poster_first == "":
        poster_first = None
    if poster_last == "":
        poster_last = None
    if poster_email == "":
        poster_email = None

    poster = Posters(poster_first=poster_first,
                     poster_last=poster_last,
                     email=poster_email)

    create_object(poster)
    return poster.id