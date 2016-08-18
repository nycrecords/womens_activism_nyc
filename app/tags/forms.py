from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class AddTagForm(Form):
    add = StringField('Please enter a tag to add:', validators=[Optional()])
    submit = SubmitField('Submit')


class RemoveTagForm(Form):
    remove = StringField('Please enter a tag to remove:', validators=[Optional()])
    submit = SubmitField('Submit')


class EditTagForm(Form):
    current = StringField('Please enter an existing tag:', validators=[Optional()])
    edit = StringField('Please enter a new tag:', validators=[Optional()])
    submit = SubmitField('Submit')


#  TODO: DOCSTRINGS