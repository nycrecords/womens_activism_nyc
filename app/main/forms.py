from flask_wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Comment(Form):
    content = StringField('Comment', validators=[DataRequired("Comment can't be left blank")])
    submit = SubmitField('submit')
