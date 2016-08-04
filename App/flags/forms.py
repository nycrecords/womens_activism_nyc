"""
Modules needed for flags/forms.py
flask_wtf:
    used class Form from which FlagsForm inherits from
wtforms:
    used SelectField for drop down list of options
    used TextAreaField for area for user's explanation
wtforms.validators:
    used Length to verify the length maximum of 500 characters
flask_wtf.recaptcha:
    used RecaptchaField for Recaptcha verificiation of form submission
"""
from flask_wtf import Form
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import Length
from flask_wtf.recaptcha import RecaptchaField

flag_choices = [('Inappropriate Content', 'Inappropriate Content'), ('Offensive Content', "Offensive Content"),
                ('Wrong Information', 'Wrong Information'), ('Other', 'Other')]


class FlagsForm(Form):
    """
    FlagsForm used for user to create a flag ticket that identifies something wrong with post/comment
    flag_reason is a drop down menu that includes all possible reasons to flag something
    flag_description is a box where a user can type their explanation for flagging something
    """
    flag_reason = SelectField('Please choose a reason for flagging:', choices=flag_choices)
    flag_description = TextAreaField('Please provide a brief description:', validators=[Length(0, 500)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
