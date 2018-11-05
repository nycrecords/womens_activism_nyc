from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)

from wtforms.validators import (
    Email,
    Length,
    Optional
)


class UnsubscribeForm(FlaskForm):
    email = StringField('Email', validators=[Optional(), Email(), Length(1, 254)])
    phone = StringField('Phone', validators=[Optional(), Length(1, 25)])
    submit = SubmitField('Unsubscribe')
