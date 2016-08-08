"""
Modules needed for feedback/views.py
flask:
    used render_template to load templates
    used redirect to redirect to specific url
    used url_for to designate the specific url
    used current_app for config data variables
    used flash to send messages to the user
app.db_helpers:
    used to add and commit sessions for Flags with the put_obj() function
app.models:
    used Feedback table to add a row of data every time user successfully submitted feedback
app.send_email:
    send_email() function defined in app/send_email.py used to send email to recipient, formats subject title and email content
app.feedback:
    used to import the feedback blueprint where routes are identified from
app.feedback.forms:
    used FeedbackForm to define object based upon the class FeedbackForms created in feedback/forms.py
"""
from flask import render_template, redirect, url_for, current_app, flash
from app.db_helpers import put_obj
from app.models import Feedback
from app.send_email import send_email
from app.feedback import feedback
from app.feedback.forms import FeedbackForm


@feedback.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """
    Function feedback will allow user to provide a subject and their general feedback about the site
    The user can also provide an email where they can be contacted at
    The view function will then commit the information of the feedback to the database
    An email will be sent to the email account of WOMENS_ADMIN detailing the information user provided
    :return: template that renders a form where user will provide their information regarding general feedback
    redirects user back to same page with empty boxes when completed
    """
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.subject.data
        email = form.email.data
        reason = form.reason.data
        feedback = Feedback(title=title, email=email, reason=reason)
        put_obj(feedback)
        send_email(to=current_app.config['WOMENS_ADMIN'],subject='New Feedback',
                   template='mail/new_feedback', feedback=feedback)
        flash('Thank you for your feedback!')
        return redirect(url_for('.feedback'))
    return render_template('feedback.html', form=form)
