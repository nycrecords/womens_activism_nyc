"""
View functions for story functionality
"""
from app.stories import stories
from flask import render_template

from app.constants.video_url import (
    YOUTUBE_FULL_URL,
    YOUTUBE_FULL_URL_SPLIT,
    YOUTUBE_EMBED_URL,
    YOUTUBE_SHORT_URL,
    VIMEO_STRING,
    VIMEO_URL,
    VIMEO_EMBED_URL
)
from app.models import Stories, Tags, Users


@stories.route('/', methods=['GET'])
def catalog():
    return render_template(
        'stories/stories.html'
    )


@stories.route('/<story_id>', methods=['GET'])
def view(story_id):
    story = Stories.query.filter_by(id=story_id).one()

    if story.is_visible:
        user = Users.query.filter_by(guid=story.user_guid).one() if story.user_guid else None

        video_url = None
        if story.video_url:
            video_url = story.video_url
            if YOUTUBE_FULL_URL in video_url:
                split = video_url.split(YOUTUBE_FULL_URL_SPLIT, 1)
                video_url = YOUTUBE_EMBED_URL.format(split[1])
            elif YOUTUBE_SHORT_URL in video_url:
                split = video_url.split(YOUTUBE_SHORT_URL, 1)
                video_url = YOUTUBE_EMBED_URL.format(split[1])
            elif VIMEO_STRING in video_url:
                split = video_url.split(VIMEO_URL, 1)
                video_url = VIMEO_EMBED_URL.format(split[1])
        return render_template('stories/view.html', story=story, user=user, video_url=video_url)
