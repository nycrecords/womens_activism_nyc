"""
View functions for story functionality
"""
from app.stories import stories
from app.edit.utils import hide_story
from app.feature.utils import hide_current_featured_story
from flask import render_template, abort, request, flash, redirect, url_for, current_app
from sqlalchemy.orm.exc import NoResultFound
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from app.edit.forms import HideForm

from datetime import datetime, timedelta

from app.constants.video_url import (
    YOUTUBE_FULL_URL,
    YOUTUBE_FULL_URL_SPLIT,
    YOUTUBE_EMBED_URL,
    YOUTUBE_SHORT_URL,
    VIMEO_STRING,
    VIMEO_URL,
    VIMEO_EMBED_URL
)
from app.models import Stories, Tags, Users, FeaturedStories


@stories.route('/catalog/', methods=['GET'])
@stories.route('/stories/', methods=['GET'])
def catalog():
    return render_template(
        'stories/stories.html',
        tags=Tags.query.order_by(Tags.name).all()
    )


@stories.route('/catalog/<story_id>', methods=['GET', 'POST'])
@stories.route('/stories/<story_id>', methods=['GET', 'POST'])
def view(story_id):
    form = HideForm(request.form)

    if request.method == 'POST':
        if request.form['submit'] == "Hide this Story":
            hide_story(story_id)
            flash("Story Hidden!", category='success')
            return redirect(url_for('stories.catalog'))
        elif request.form['submit'] == "Remove this Featured Story":
            hide_current_featured_story(story_id)
            flash("This story is now hidden from the Featured Stories", category='success')
            return redirect(url_for('main.index'))

    else:
        try:
            story = Stories.query.filter_by(id=story_id).one()
            assert story.is_visible
        except NoResultFound:
            print("Story does not exist")
            return abort(404)
        except AssertionError:
            print("Story is not visible")
            return abort(404)

        user = Users.query.filter_by(guid=story.user_guid).one() if story.user_guid else None
        feature = FeaturedStories.query.filter_by(story_id=story.id).one_or_none()

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

        image_url = None
        if story.image_blob_name:
            sas_token = generate_blob_sas(
                account_name=current_app.config['AZURE_STORAGE_ACCOUNT_NAME'],
                account_key=current_app.config['AZURE_STORAGE_ACCOUNT_KEY'],
                container_name=current_app.config['AZURE_CONTAINER_NAME'],
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1),
                blob_name=story.image_blob_name
            )
            image_url = "https://{0}.blob.core.windows.net/{1}/{2}?{3}".format(
                current_app.config["AZURE_STORAGE_ACCOUNT_NAME"],
                current_app.config["AZURE_CONTAINER_NAME"],
                story.image_blob_name,
                sas_token,
            )
        elif story.image_url != "":
            image_url = story.image_url
        else:
            pass
            
        return render_template('stories/view.html', story=story, user=user, image_url=image_url, video_url=video_url,
                               feature=feature, form=form)
