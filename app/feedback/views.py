from flask import render_template, redirect, url_for, current_app, flash
from .. import db
from ..models import *
from ..send_email import send_email
from . import feedback
from .forms import FeedbackForm


@feedback.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.subject.data
        email = form.email.data
        reason = form.reason.data
        feedback = Feedback(title=title, email=email, reason=reason)
        db.session.add(feedback)
        db.session.commit()
        send_email(to=current_app.config['WOMENS_ADMIN'],subject='New Feedback',
                   template='mail/new_feedback', feedback=feedback)
        flash('Thank you for your feedback!')
        return redirect(url_for('.feedback'))
    return render_template('feedback.html', form=form)