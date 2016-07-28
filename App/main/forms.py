from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_pagedown.fields import PageDownField
from flask_wtf.recaptcha import RecaptchaField


class FeedbackForm(Form):
    subject = StringField('Subject', validators=[DataRequired("Please enter the subject.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email()])
    reason = TextAreaField('Comments', validators=[DataRequired("Please enter your report.")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired('Please enter a title')])
    content = PageDownField("What's on your mind?", validators=[DataRequired("Body can't be left blank")])
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')