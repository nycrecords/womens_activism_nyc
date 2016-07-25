from flask import Flask, render_template, request, flash
from .forms import FeedbackForm
from flask import current_app
from app.email_noficiation import send_email
from ..models import Feedback
from . import main
# from ..import db
# from forms import Feedbackform
# from flask_mail import Mail, Message
# from ..email_notification import send_email


# main = Flask(__name__)

@main.route('/', methods=['GET','POST'])
def index():
    form = FeedbackForm()
    return render_template('index.html', form=form)
# the tabs on the top


@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
# replace user with feedback
    if form.validate_on_submit():
        flash("We received your feedback, Thanks! ")
        feedback = Feedback(email=form.email.data.lower(),
                title=form.subject.data,
                reason=form.reason.data)

        current_app.logger.info("Subject: {}\nEmail: {}\nReason: {}\n".format(form.subject.data, form.email.data, form.reason.data))

        send_email(to=feedback.email, subject='Subject', template='email_feedback',

                   reason=feedback.reason,
                   title=feedback.title
                   )
        return render_template('index.html', form=form)
    else:
        return render_template('index.html', form=form)
