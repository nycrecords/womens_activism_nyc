"""
Modules for post/forms.py
flask_wtf: wrapper class for WTForms
WTForms: used to create web forms for Users
WTForms.validators: used to validate the fields in the
flask_wtf.recaptcha: used to implement reCAPTCHA functionality into the WTForms
"""
from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.recaptcha import RecaptchaField


class CommentForm(Form):
    content = TextAreaField('Enter your comment', validators=[DataRequired("Comment can't be left blank")])
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')


class CommentEditForm(Form):
    reason = TextAreaField('Reason', validators=[DataRequired("Reason can't be left blank")])
    content = TextAreaField('Comment Content', validators=[DataRequired("Comment can't be left blank")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

