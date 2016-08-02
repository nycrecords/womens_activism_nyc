from flask_wtf import Form 
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired 
from flask_wtf.recaptcha import RecaptchaField


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired('Please enter a title')])
    content = TextAreaField("What's on your mind?", validators=[DataRequired("Body can't be left blank")])
    # recaptcha = RecaptchaField()
    submit = SubmitField('submit')


class DeleteForm(Form):
    submit = SubmitField('submit')