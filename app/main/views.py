from flask import render_template, redirect, url_for
from .. import db
from ..models import Feedback
from ..email import send_email
from . import main
from .forms import FeedbackForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()

    if form.validate_on_submit():
        subject = form.subject.data
        email = form.email.data
        reason = form.reason.data
        print('Subject: {}\nEmail: {}\nReason: {}'.format(subject, email, reason))

        feedback = Feedback(title=subject, email=email, reason=reason)
        db.session.add(feedback)
        return redirect(url_for('.index'))

    return render_template('index.html', form=form)