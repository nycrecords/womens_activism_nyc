"""
Custom validators used to validate fields in the WTForm
"""

from wtforms import ValidationError
import requests


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
    if activist_end != "Today" and activist_end != "today" and not activist_end.isdigit():
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