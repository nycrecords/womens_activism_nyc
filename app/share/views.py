from flask import render_template, redirect, url_for, flash, request, Markup

from app.constants import RECAPTCHA_STRING
from app.lib.utils import create_story, create_user, create_subscriber
from app.models import Tags
from app.share import share
from app.share.forms import StoryForm

from config import Config

import requests

@share.route('/', methods=['GET', 'POST'])
def new():
    """
    View function for creating a story
    :return: If the story form was fully validated, create a Story and Poster object to store in the database
    """
    form = StoryForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.user_first.data
            last_name = form.user_last.data
            email = form.user_email.data
            phone = form.user_phone.data

            # Verify recaptcha token and return error if failed
            recaptcha_response = requests.post(url=f'https://www.google.com/recaptcha/api/siteverify?secret={ Config.RECAPTCHA_PRIVATE_KEY }&response={ request.form["g-recaptcha-response"] }').json()
            if recaptcha_response['success'] is False or recaptcha_response['score'] < 0.5:
                flash(Markup('Recaptcha failed to validate you!'), category='danger')

                return render_template('share/share.html', form=form, tags=Tags.query.order_by(Tags.name).all(),
                                       RECAPTCHA_PUBLIC_KEY=Config.RECAPTCHA_PUBLIC_KEY)

            # Create new user and subscriber
            if first_name or last_name or email:
                user_guid = create_user(user_first=first_name,
                                        user_last=last_name,
                                        user_email=email,
                                        user_phone=phone)
                if form.subscription.data and (email or phone):
                    create_subscriber(first_name=first_name,
                                      last_name=last_name,
                                      email=email,
                                      phone=phone)
            else:
                user_guid = None

            tag_string = form.tags.data
            tags = []
            for t in tag_string.split(','):
                tags.append(Tags.query.filter_by(id=t).one().name)

            story_id = create_story(activist_first=form.activist_first.data,
                                    activist_last=form.activist_last.data,
                                    activist_start=form.activist_start.data,
                                    activist_end=form.activist_end.data,
                                    tags=tags,
                                    content=form.content.data,
                                    activist_url=form.activist_url.data,
                                    image_url=form.image_url.data,
                                    video_url=form.video_url.data,
                                    user_guid=user_guid)
            flash(Markup('Story submitted!'), category='success')
            return redirect(url_for('stories.view', story_id=story_id))
        else:
            for field, error in form.errors.items():
                if field == RECAPTCHA_STRING:
                    flash('Please complete the RECAPTCHA to submit your story.', category="danger")
                else:
                    flash(form.errors[field][0], category="danger")
            return render_template('share/share.html', form=form, tags=Tags.query.order_by(Tags.name).all(), RECAPTCHA_PUBLIC_KEY=Config.RECAPTCHA_PUBLIC_KEY)
    return render_template('share/share.html', form=form, tags=Tags.query.order_by(Tags.name).all(), RECAPTCHA_PUBLIC_KEY=Config.RECAPTCHA_PUBLIC_KEY)
