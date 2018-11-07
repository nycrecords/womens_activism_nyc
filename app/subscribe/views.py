from flask import render_template, flash, request, Markup, redirect, url_for

from app.lib.utils import create_subscriber
from app.subscribe import subscribe
from app.subscribe.forms import SubscribeForm


@subscribe.route('/', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.user_first.data
            last_name = form.user_last.data
            email = form.user_email.data
            phone = form.user_phone.data

            if email or phone:
                create_subscriber(first_name=first_name,
                                  last_name=last_name,
                                  email=email,
                                  phone=phone)
                flash(Markup('Thank you for subscribing!'), category='success')
                return redirect(url_for('subscribe.subscribe'))
            else:
                flash(Markup('Please enter an email address or phone number.'), category='warning')
                return redirect(url_for('subscribe.subscribe'))
    else:
        return render_template('subscribe/subscribe.html', form=form)
