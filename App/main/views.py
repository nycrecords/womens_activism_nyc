from flask import render_template, flash, current_app, session, redirect, url_for
from .forms import FeedbackForm, FlagsForm
from App.email_notification import send_email
from ..models import Feedback, Flag
from . import main

post_title = 'The Life of Harriet Tubman'


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        flash("We received your feedback, Thanks!")
        feedback = Feedback(email=form.email.data.lower(),
                            title=form.subject.data,
                            reason=form.reason.data)
        current_app.logger.info(
            "Subject: {}\nEmail: {}\nReason: {}\n".format(form.subject.data, form.email.data, form.reason.data))
        send_email(to=feedback.email, subject='Feedback', template='email_feedback',
                   reason=feedback.reason, title=feedback.title)
        return redirect(url_for('main.feedback'))
    else:
        return render_template('feedback.html', form=form)


@main.route('/flags', methods=['GET', 'POST'])
def flags():
    form = FlagsForm()
    # On final build there should be a variable "post_title" gotten from calling DB/URL/etc
    if form.validate_on_submit():
        flash('Thanks for your input, a moderator has been notified')
        flags = Flag(type=form.flag_reason.data,
                     reason=form.flag_description.data)
        current_app.logger.info(
            "Flag_reason: {}\nFlag_description: {}".format(form.flag_reason.data, form.flag_description.data))
        send_email(to=current_app.config['FLAG_MAIL_ADMIN'], subject='Flag', template='email_flags',
                   reason=flags.type, description=flags.reason)
        return redirect(url_for('main.flags'))
    else:
        return render_template('flags.html', form=form, post_title=post_title)






