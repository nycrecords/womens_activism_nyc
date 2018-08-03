from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
)

class ExportForm(FlaskForm):
    submit = SubmitField('Submit')