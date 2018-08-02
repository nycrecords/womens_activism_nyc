from flask import render_template, flash, request, Markup

from app.unsubscribe import unsubscribe
from app.unsubscribe.forms import UnsubscribeForm
from app.edit.utils import update_user
from app.models import Users
from app.lib.emails_utils import send_email


@unsubscribe.route('/', methods=['GET', 'POST'])
def unsubscribe():
    form = UnsubscribeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.user_email.data:
                user = Users.query.filter_by(email=form.user_email.data, subscription=True).one_or_none()
                if user is None:
                    email_body = render_template('emails/remove_subscriber_agency.html',
                                                 first_name=user.first_name,
                                                 last_name=user.last_name,
                                                 email=form.user_email.data)
                    send_email(subject="WomensActivism - Remove Subscriber",
                               sender=current_app.config['MAIL_SENDER'],
                               recipients=[current_app.config['MAIL_RECIPIENTS']],
                               html_body=email_body)
                else:
                    update_user(user,
                            user.first_name,
                            user.last_name,
                            form.user_email.data,
                            False)
            flash(Markup('You are no longer subscribed.'), category='success')
            return render_template('unsubscribe/unsubscribe.html', form=form)
    return render_template('unsubscribe/unsubscribe.html', form=form)
