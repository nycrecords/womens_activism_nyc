from flask import render_template, flash, request, Markup, redirect, url_for

from app.lib.utils import create_subscriber
from app.subscribe import subscribe
from app.subscribe.forms import SubscribeForm

from config import Config

import requests

@subscribe.route('/', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.user_first.data
            last_name = form.user_last.data
            email = form.user_email.data
            phone = form.user_phone.data

            # Verify recaptcha token
            recaptcha_response = requests.post(url=f'https://www.google.com/recaptcha/api/siteverify?secret={ Config.RECAPTCHA_PRIVATE_KEY }&response={ request.form["g-recaptcha-response"] }').json()

            if not (email or phone):
                flash(Markup('Please enter an email address or phone number.'), category='warning')

            elif recaptcha_response['success'] is False or recaptcha_response['score'] < 0.5:
                flash(Markup('Recaptcha failed to validate you!'), category='danger')

            else:
                create_subscriber(first_name=first_name,
                                  last_name=last_name,
                                  email=email,
                                  phone=phone)
                flash(Markup('Thank you for subscribing!'), category='success')

            return redirect(url_for('subscribe.subscribe'))
    else:
        return render_template('subscribe/subscribe.html', form=form, RECAPTCHA_PUBLIC_KEY=Config.RECAPTCHA_PUBLIC_KEY)
