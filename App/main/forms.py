from flask_wtf import Form, RecaptchaField
from wtforms import SelectField, SubmitField, TextAreaField, StringField, validators
from wtforms.validators import DataRequired, Length

flag_choices = [('inappropriate', 'Inappropriate content'), ('offensive', "Offensive content"), ('incorrect', 'Incorrect information'), ('other', 'Other')]


class FeedbackForm(Form):
    subject = StringField('What is the subject', validators=[DataRequired("Please enter the subject")])
    email = StringField('What is your email?', validators=[validators.email()])
    reason = TextAreaField('Reason for report?', validators=[DataRequired("Please enter your report")])
    submit = SubmitField('Submit')


class FlagsForm(Form):
    flag_reason = SelectField('Reason for flagging?', choices=flag_choices, validators=[DataRequired('Please Select a reason')])
    flag_description = TextAreaField('Please provide a brief description', validators=[Length(0, 500)])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')