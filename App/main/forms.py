from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class FeedbackForm(Form):
    subject = StringField('What is the subject', validators=[DataRequired("Please enter the subject")])
    email = StringField('What is your email?', validators=[DataRequired("Please enter your email")])
    reason = TextAreaField('Reason for report?', validators=[DataRequired("Please enter your report")])
    submit = SubmitField('Submit')


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired('Please enter a title')])
    content = TextAreaField("What's on your mind?", validators=[DataRequired("Body can't be left blank")])
    submit = SubmitField('submit')