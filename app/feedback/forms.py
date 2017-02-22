"""
Modules needed for feedback/forms.py
flask_wtf:
    used class Form from which FeedbackForm inherits from
wtforms:
    used Stringfield for area for user's input (subject of feedback)
    used TextAreaField for larger area for user's explanation (actual feedback)
    used SubmitField for submit button
wtforms.validators:
    used Length to verify the length maximum of 500 characters
    used DataRequired for verification that user inputted information
    used Email for verification that user inputted a proper email
flask_wtf.recaptcha:
    used RecaptchaField for Recaptcha verification of form submission
"""
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.recaptcha import RecaptchaField


class FeedbackForm(Form):
    """
    Feedback form used for user to submit general feedback about the site to the admin
    subject is where user identifies the subject/nature of feedback
    email is where user provides an email where they can be contacted
    reason is where user provides the bulk of information/explanation about their feedback
    """
    subject = StringField('Subject', validators=[DataRequired("Please enter the subject."), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email(), Length(1, 64)])
    reason = TextAreaField('Comments', validators=[DataRequired("Please enter your report."), Length(1, 500)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
