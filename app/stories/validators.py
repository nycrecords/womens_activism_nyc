from wtforms import ValidationError
import requests


def validate_name(form, name):
    activist_name = name.data
    if activist_name[:1].islower():
        raise ValidationError()


def validate_start_year(form, year):
    activist_start = year.data
    if not activist_start.isdigit():
        raise ValidationError()


def validate_end_year(form, year):
    activist_end = year.data
    if activist_end != "Today" and (activist_end.isdigit() == False):
        raise ValidationError()


def validate_url(form, url):
    try:
        url_test = requests.get(url.data)
        if url_test.status_code != 200:
            raise ValidationError()
    except:
        raise ValidationError()


def validate_image(form, image):
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
    print(video.data)
    if "youtube.com" in video.data or "youtu.be" in video.data or "vimeo.com" in video.data:
        try:
            video_test = requests.get(video.data)
            if video_test.status_code != 200:
                raise ValidationError('Invalid video URL, please try again.')
        except:
            raise ValidationError('Invalid video URL, please try again.')
    else:
        raise ValidationError('Invalid video URL, please try again.')