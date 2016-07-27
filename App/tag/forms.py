from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class TagForm(Form):
    add = StringField('Add', validators=[Optional()])
    remove = StringField('Delete', validators=[Optional()])
    current = StringField('Current', validators=[Optional()])
    edit = StringField('edit', validators=[Optional()])
    submit = SubmitField('Submit')