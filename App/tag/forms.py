from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class TagForm(Form):
    add = StringField('Add', validators=[Optional()])
    remove = StringField('Delete', validators=[Optional()])
    submit = SubmitField('Submit')