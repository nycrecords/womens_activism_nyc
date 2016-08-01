from flask_wtf import Form
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.recaptcha import RecaptchaField

flag_choices = [('Inappropriate Content', 'Inappropriate Content'), ('Offensive Content', "Offensive Content"),
                ('Incorrect Information', 'Incorrect Information'), ('Other', 'Other')]


class FlagsForm(Form):
    flag_reason = SelectField('Please choose a reason for flagging:', choices=flag_choices,
                              validators=[DataRequired('Please select a reason.')])
    flag_description = TextAreaField('Please provide a brief description:', validators=[Length(0, 500)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')