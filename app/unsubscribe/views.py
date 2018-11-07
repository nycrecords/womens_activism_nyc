from flask import render_template, flash, request, Markup, redirect, url_for

from app.lib.utils import remove_subscriber
from app.unsubscribe import unsubscribe
from app.unsubscribe.forms import UnsubscribeForm


@unsubscribe.route('/', methods=['GET', 'POST'])
def unsubscribe():
    form = UnsubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            phone = form.phone.data

            if email or phone:
                remove_subscriber(email, phone)
                flash(Markup("You are no longer subscribed."), category='success')
            else:
                flash("Please enter an email address or phone number.", category='warning')
            return redirect(url_for('unsubscribe.unsubscribe'))
    else:
        return render_template('unsubscribe/unsubscribe.html', form=form)
