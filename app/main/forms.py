# TODO: Add module documentation
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, Email


class FeedbackForm(Form):
    subject = StringField('What is the subject', validators=[DataRequired("Please enter the subject")])
    email = StringField('What is your email?', validators=[validators.Email()])
    reason = TextAreaField('Reason for report?', validators=[DataRequired("Please enter your report")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
