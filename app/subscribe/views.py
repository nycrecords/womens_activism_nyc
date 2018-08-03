from flask import render_template, flash, request, Markup, redirect, url_for, current_app

from app.subscribe import subscribe
from app.subscribe.forms import SubscribeForm
from app.lib.utils import create_user
from app.lib.emails_utils import send_email
from app.models import Events
from app.db_utils import create_object
from app.constants.event import EMAIL_SENT


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
                                        user_phone=form.user_phone.data,
                                        subscription=True)
                # Email for the admin
                email_body = render_template('emails/new_subscriber_agency.html',
                                             first_name=form.user_first.data,
                                             last_name=form.user_last.data,
                                             email=form.user_email.data,
                                             phone=form.user_phone.data)
                send_email(subject="WomensActivism - New Subscriber",
                           sender=current_app.config['MAIL_SENDER'],
                           recipients=[current_app.config['MAIL_RECIPIENTS']],
                           html_body=email_body)
                create_object(Events(
                    _type=EMAIL_SENT,
                    user_guid=user_guid,
                    new_value={"email_body": email_body}
                ))
                # Email for the user
                if form.user_email.data:
                    unsubscribe_link = url_for('unsubscribe.unsubscribe', _external=True)
                    email_user_body = render_template('emails/new_subscriber_user.html',
                                                      first_name=form.user_first.data,
                                                      last_name=form.user_last.data,
                                                      unsubscribe_link = unsubscribe_link)
                    send_email(subject="Confirmation Email",
                               sender=current_app.config['MAIL_SENDER'],
                               recipients=[form.user_email.data],
                               html_body=email_user_body)
                    create_object(Events(
                        _type=EMAIL_SENT,
                        user_guid=user_guid,
                        new_value={"email_body": email_body}
                    ))
                flash(Markup('Thank you for subscribing!'), category='success')
                return redirect(url_for('subscribe.subscribe'))
            else:
                flash(Markup('Please enter an email or phone number.'), category='danger')
                return redirect(url_for('subscribe.subscribe'))

    return render_template('subscribe/subscribe.html', form=form)
