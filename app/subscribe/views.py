from flask import render_template, flash, request, Markup, redirect, url_for

from app.subscribe import subscribe
from app.subscribe.forms import SubscribeForm
from app.lib.utils import create_user


@subscribe.route('/', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.user_email.data or form.user_phone.data:
                create_user(user_first=form.user_first.data,
                            user_last=form.user_last.data,
                            user_email=form.user_email.data,
                            user_phone=form.user_phone.data,
                            subscription=True)
                flash(Markup('Thank you for subscribing!'), category='success')
                return redirect(url_for('subscribe.subscribe'))
            else:
                flash(Markup('Please enter an email or phone number.'), category='danger')
                return redirect(url_for('subscribe.subscribe'))
    return render_template('subscribe/subscribe.html', form=form)
