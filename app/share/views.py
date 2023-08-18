from flask import render_template, redirect, url_for, flash, request, Markup, current_app, escape

from app.constants.subscribe_status import EMAIL_INVALID, EMAIL_TAKEN, PHONE_TAKEN, PHONE_INVALID
from app.lib.utils import create_story, create_user, create_subscriber, verify_subscriber
from app.models import Tags
from app.share import share
from app.share.forms import StoryForm

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
            first_name = escape(form.user_first.data)
            last_name = escape(form.user_last.data)
            email = escape(form.user_email.data)
            phone = escape(form.user_phone.data)

            if current_app.config['RECAPTCHA_ENABLED']:
                # Verify recaptcha token and return error if failed
                recaptcha_response = requests.post(
                    url='https://www.google.com/recaptcha/api/siteverify?secret={}&response={}'
                        .format(current_app.config["RECAPTCHA_PRIVATE_KEY"],
                                request.form["g-recaptcha-response"])).json()

                if recaptcha_response['success'] is False or recaptcha_response['score'] < current_app.config[
                    "RECAPTCHA_THRESHOLD"]:
                    flash(Markup('Recaptcha failed, please try again.'), category='danger')
                    return render_template('share/share.html', form=form, tags=Tags.query.order_by(Tags.name).all(),
                                           RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

            # Create new user and subscriber
            if first_name or last_name or email or phone:
                user_guid = create_user(user_first=escape(first_name),
                                        user_last=escape(last_name),
                                        user_email=escape(email),
                                        user_phone=escape(phone))

                # Check entered email and phone number
                if form.subscription.data and (email or phone):
                    verify = verify_subscriber(email, phone)

                    if verify == EMAIL_TAKEN:
                        flash(Markup('The email you entered is already subscribed, please use another email.'),
                              category='warning')
                        return render_template('share/share.html', form=form,
                                               RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                    elif verify == PHONE_TAKEN:
                        flash(
                            Markup(
                                'The phone number you entered is already subscribed, please use another phone number.'),
                            category='warning')
                        return render_template('share/share.html', form=form,
                                               RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                    elif verify == EMAIL_INVALID:
                        flash(Markup('The email you entered isn\'t valid, please use another email.'),
                              category='danger')
                        return render_template('share/share.html', form=form,
                                               RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                    elif verify == PHONE_INVALID:
                        flash(Markup('The phone number you entered isn\'t valid, please use another phone number.'),
                              category='danger')
                        return render_template('share/share.html', form=form,
                                               RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                    # Valid email; Create subscriber
                    else:
                        create_subscriber(escape(first_name=first_name),
                                          escape(last_name=last_name),
                                          escape(email=email),
                                          escape(phone=phone))
            else:
                user_guid = None

            tag_string = form.tags.data
            tags = []
            for t in tag_string.split(','):
                tags.append(Tags.query.filter_by(id=t).one().name)

            story_id = create_story(activist_first=escape(form.activist_first.data),
                                    activist_last=escape(form.activist_last.data),
                                    activist_start=escape(form.activist_start.data),
                                    activist_end=escape(form.activist_end.data),
                                    tags=tags,
                                    content=escape(form.content.data),
                                    activist_url=escape(form.activist_url.data),
                                    image_url=escape(form.image_url.data),
                                    video_url=escape(form.video_url.data),
                                    user_guid=user_guid)
            flash(Markup('Story submitted!'), category='success')
            return redirect(url_for('stories.view', story_id=story_id))
        else:
            for field, error in form.errors.items():
                flash(form.errors[field][0], category="danger")
            return render_template('share/share.html', form=form, tags=Tags.query.order_by(Tags.name).all(),
                                   RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])
    return render_template('share/share.html', form=form, tags=Tags.query.order_by(Tags.name).all(),
                           RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])
