from flask import render_template, flash, request, Markup, redirect, url_for, current_app

from app.constants.subscribe_status import EMAIL_INVALID, EMAIL_TAKEN, PHONE_TAKEN, PHONE_INVALID
from app.lib.utils import create_subscriber, verify_subscriber
from app.subscribe import subscribe
from app.subscribe.forms import SubscribeForm

import requests


@subscribe.route('/', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.user_first.data
            last_name = form.user_last.data
            email = form.user_email.data.lower()
            phone = form.user_phone.data

            if current_app.config['RECAPTCHA_ENABLED']:
                # Verify recaptcha token
                recaptcha_response = requests.post(
                    url='https://www.google.com/recaptcha/api/siteverify?secret={}&response={}'.format(
                        current_app.config['RECAPTCHA_PRIVATE_KEY'], request.form["g-recaptcha-response"])).json()

                if recaptcha_response['success'] is False or recaptcha_response['score'] < current_app.config[
                    "RECAPTCHA_THRESHOLD"]:
                    flash(Markup('Recaptcha failed, please try again.'), category='danger')
                    return render_template('subscribe/subscribe.html', form=form,
                                           RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

            if not (email or phone):
                flash(Markup('Please enter an email address or phone number.'), category='warning')
            else:
                # Check entered email and phone number
                verify = verify_subscriber(email, phone)

                if verify == EMAIL_TAKEN:
                    flash(Markup('The email you entered is already subscribed, please use another email.'),
                          category='warning')
                    return render_template('subscribe/subscribe.html', form=form,
                                           RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                elif verify == PHONE_TAKEN:
                    flash(
                        Markup('The phone number you entered is already subscribed, please use another phone number.'),
                        category='warning')
                    return render_template('subscribe/subscribe.html', form=form,
                                           RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                elif verify == EMAIL_INVALID:
                    flash(Markup('The email you entered isn\'t valid, please use another email.'), category='danger')
                    return render_template('subscribe/subscribe.html', form=form,
                                           RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                elif verify == PHONE_INVALID:
                    flash(Markup('The phone number you entered isn\'t valid, please use another phone number.'),
                          category='danger')
                    return render_template('subscribe/subscribe.html', form=form,
                                           RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])

                # Valid email; Create subscriber
                else:
                    create_subscriber(first_name=first_name,
                                      last_name=last_name,
                                      email=email,
                                      phone=phone)
                    flash(Markup('Thank you for subscribing!'), category='success')

            return redirect(url_for('subscribe.subscribe'))
    else:
        return render_template('subscribe/subscribe.html', form=form,
                               RECAPTCHA_PUBLIC_KEY=current_app.config['RECAPTCHA_PUBLIC_KEY'])
