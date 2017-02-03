from app.models import Stories, Posters
from app import db
from flask import session


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
        activist_start *= -1
    if activist_end_BC:
        activist_end *= -1
    if activist_end == "Today":
        activist_end = 9999

    story = Stories(activist_first=activist_first,
                    activist_last=activist_last,
                    activist_start=activist_start,
                    activist_end=activist_end,
                    content=content,
                    activist_url=activist_url,
                    image_url=image_url,
                    video_url=video_url,
                    poster_id=poster_id)

    db.session.add(story)
    db.session.commit()


def create_poster(poster_first,
                  poster_last,
                  poster_email):
    poster = Posters(poster_first=poster_first,
                     poster_last=poster_last,
                     email=poster_email)
    db.session.add(poster)
    db.session.commit()
    return poster.id