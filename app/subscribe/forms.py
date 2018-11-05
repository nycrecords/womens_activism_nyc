from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    Email,
)


class SubscribeForm(FlaskForm):
    """
    The WTForm used to create a new Story
    """
    user_first = StringField("User first name", validators=[Optional(), Length(1, 128)])
    user_last = StringField("User last name", validators=[Optional(), Length(1, 128)])
    user_email = StringField("User email", validators=[Optional(), Email(), Length(1, 254)])
    user_phone = StringField("User phone number", validators=[Optional(), Length(1, 25)])
    submit = SubmitField('Submit')
