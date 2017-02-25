"""
Custom validators used to validate fields in the WTForm
"""

from wtforms import ValidationError
import requests


def validate_user(user_first, user_last):
    """
    A validator used check that a poster has provided both their first and last name if they decide to
    give their personal information.

    :param user_first: the poster's first name
    :param user_last: the poster's last name
    :return: True is validation is passed, False otherwise
    """
    if (len(user_first) == 0 and len(user_last) != 0) or (len(user_first) != 0 and len(user_last) == 0):
        return False
    else:
        return True


def validate_years(activist_start, activist_start_BC, activist_end, activist_end_BC):
    """
    A validator used to to check edge cases for activist years involving both the start and end years.

    :param activist_start: the activist's birth year
    :param activist_start_BC: a boolean to see if the birth year was a BC year
    :param activist_end: the activist's death year
    :param activist_end_BC: a boolean to see if the death year was a BC year
    :return: True is the years are valid, False otherwise
    """
    # ensure "Today" and BC are not inputted at the same time
    if (activist_end == "Today" or activist_end == "today") and activist_end_BC:
        return False

    # if the activist years are BC years then convert them to negative integers
    if activist_start_BC:
        activist_start = int(activist_start) * -1
    if activist_end_BC:
        activist_end = int(activist_end) * -1

    if activist_start > activist_end:
        return False
    return True


def validate_start_year(form, year):
    """
    A validator to check that the start year is only numbers
    :param form: part of the StoryForm
    :param year: the start year that will be validated
    """
    activist_start = year.data
    activist_start.strip()
    if not activist_start.isdigit():
        raise ValidationError()


def validate_end_year(form, year):
    """
    A validator to check that the start year is only numbers or "Today"
    :param form: part of the StoryForm object
    :param year: the end year that will be validated
    """
    activist_end = year.data
    activist_end.strip()
    if activist_end != "Today" and activist_end != "today" and activist_end.isdigit() == False:
        raise ValidationError()


def validate_url(form, url):
    """
    A validator to check that the url is valid and returns a 200 response code

    :param form: part of the StoryForm object
    :param url: a url with additional information about an activist
    """
    try:
        url_test = requests.get(url.data)
        if url_test.status_code != 200:
            raise ValidationError()
    except:
        raise ValidationError()


def validate_image(form, image):
    """
    A validator to check that an image URL has the proper format and returns a 200 response code

    :param form: part of the StoryForm object
    :param image: the URL of the image
    """
    if (image.data[-3:].lower() == 'jpg') or (image.data[-3:].lower() == 'png') or (image.data[-4:].lower() == 'jpeg'):
        try:
            image_test = requests.get(image.data)
            if image_test.status_code != 200:
                raise ValidationError('Invalid image URL, please try again.')
        except:
            raise ValidationError('Invalid image URL, please try again.')
    else:
        raise ValidationError('The image URL must end in "jpeg","jpg", or "png". Please try again.')


def validate_video(form, video):
    """
    A validator to check that a video URL has the proper format and returns a 200 response code

    :param form: part of the StoryForm object
    :param video: the URL of the video
    """
    if "youtube.com" in video.data or "youtu.be" in video.data or "vimeo.com" in video.data:
        try:
            video_test = requests.get(video.data)
            if video_test.status_code != 200:
                raise ValidationError('Invalid video URL, please try again.')
        except:
            raise ValidationError('Invalid video URL, please try again.')
    else:
        raise ValidationError('Invalid video URL, please try again.')