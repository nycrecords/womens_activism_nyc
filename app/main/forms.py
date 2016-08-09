from flask_wtf import Form 
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired 
from flask_wtf.recaptcha import RecaptchaField


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired('Please enter a title')])
    content = PageDownField("What's on your mind?", validators=[DataRequired("Body can't be left blank")])
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')


class Comment(Form):
    content = StringField('Comment', validators=[DataRequired("Comment can't be left blank")])
    submit = SubmitField('submit')

