"""
flask_wtf:
    used class Form from which Comment inherits from
wtforms:
    used Stringfield for area for user's input (comment on a post)
    used SubmitField for submit button
wtforms.validators:
    used DataRequired for verification that user inputted information
"""
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Comment(Form):
    """
    Comment form used for user to submit a comment on a post
    content is the plaintext information that the user inputs
    """
    content = StringField('Comment', validators=[DataRequired("Comment can't be left blank")])
    submit = SubmitField('submit')

