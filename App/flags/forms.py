from flask_wtf import Form
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.recaptcha import RecaptchaField

flag_choices = [('inappropriate', 'Inappropriate content'), ('offensive', "Offensive content"), ('incorrect', 'Incorrect information'), ('other', 'Other')]


class FlagsForm(Form):
    flag_reason = SelectField('Reason for flagging?', choices=flag_choices, validators=[DataRequired('Please Select a reason')])
    flag_description = TextAreaField('Please provide a brief description', validators=[Length(0, 500)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')