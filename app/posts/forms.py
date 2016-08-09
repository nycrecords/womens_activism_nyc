from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.recaptcha import RecaptchaField


class CommentForm(Form):
    content = TextAreaField('Enter your comment', validators=[DataRequired("Comment can't be left blank")])
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')
