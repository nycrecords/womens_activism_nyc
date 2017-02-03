from app.models import Stories, Posters
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
                 poster_id):
    if activist_start_BC:
        activist_start = int(activist_start) * -1
    if activist_end_BC:
        activist_end = int(activist_end) * -1
    if activist_end == "Today":
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
