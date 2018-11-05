from flask import render_template, flash, request, Markup, current_app, redirect, url_for

from app.unsubscribe import unsubscribe
from app.unsubscribe.forms import UnsubscribeForm
from app.edit.utils import update_user
from app.models import Users, Events
from app.lib.emails_utils import send_email
from app.constants.event_type import EMAIL_SENT
from app.db_utils import create_object
from app.lib.utils import remove_subscriber


@unsubscribe.route('/', methods=['GET', 'POST'])
def unsubscribe():
    form = UnsubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            phone = form.phone.data

            if email or phone:
                remove_subscriber(email, phone)

                flash(Markup('You are no longer subscribed.'), category='success')
            else:
                flash("No subscription found.", category='warning')
            return redirect(url_for('unsubscribe.unsubscribe'))
    else:
        return render_template('unsubscribe/unsubscribe.html', form=form)
