from flask_wtf import Form 
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from ..models import Tag

class Comment(Form):
    content = StringField('Comment', validators=[DataRequired("Comment can't be left blank")])
    submit = SubmitField('submit')


class TagForm(Form):
    # for tag in Tag.query.all():
    #     tag.name = BooleanField(tag.name)
    tag1 = BooleanField('tag1')
    tag2 = BooleanField('tag2')