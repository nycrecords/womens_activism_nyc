from flask import render_template, redirect, url_for, flash, request, Markup

from app.constants import RECAPTCHA_STRING
from app.subscribe import subscribe
from app.subscribe.forms import SubscribeForm
from app.subscribe.utils import create_user

@subscribe.route('/', methods=['GET', 'POST'])
def subscribe():
    # return render_template('subscribe/subscribe.html')
    form = SubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.user_email.data or form.user_phone.data:
                user_guid = create_user(user_first=form.user_first.data,
                                        user_last=form.user_last.data,
                                        user_email=form.user_email.data,
                                        user_phone=form.user_phone.data)
                flash(Markup('Thank you for subscribing!'), category='success')
            else:
                flash(Markup('Please enter an email or phone number.'),category='danger')


    return render_template('subscribe/subscribe.html', form=form)