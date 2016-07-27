# TODO: Add module documentation
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, Length
from flask_wtf.recaptcha import RecaptchaField


# bars for website


class FeedbackForm(Form):
   subject = StringField('What is the subject', validators=[DataRequired("Please enter the subject")])
   email = StringField('What is your email?', validators=[validators.Email()])
   reason = TextAreaField('Reason for report?', validators=[Length(0, 500)])
   recaptcha = RecaptchaField()
   submit = SubmitField('Submit')