from flask import render_template, redirect, url_for, current_app, flash
from .. import db
from ..models import Feedback
from ..email import send_email
from . import main
from .forms import FeedbackForm
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        subject = form.subject.data
        email = form.email.data
        reason = form.reason.data
        print('Subject: {}\nEmail: {}\nReason: {}'.format(subject, email, reason))

        feedback = Feedback(title=subject, email=email, reason=reason)
        db.session.add(feedback)

        send_email(current_app.config['WOMENS_ADMIN'],'New Feedback', 'mail/new_user', feedback=feedback)

        flash('Thank you for your feedback!')
        return redirect(url_for('.feedback'))

    return render_template('feedback.html', form=form)


@main.route('/secret', methods=['GET', 'POST'])
@login_required
def secret():
    return render_template('secret.html')