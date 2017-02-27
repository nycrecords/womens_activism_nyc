"""
WTForms used for Stories
"""
from flask_wtf import Form
from wtforms import (
    TextAreaField,
    StringField,
    SubmitField,
    BooleanField,
)
from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    Email
)

from app.share.validators import (validate_end_year,
                                  validate_image,
                                  validate_start_year,
                                  validate_url,
                                  validate_video)


class StoryForm(Form):
    """
    The WTForm used to create a new Story
    """
    activist_first = StringField("Activist first name", validators=[DataRequired(), Length(1, 128)])
    activist_last = StringField("Activist last name", validators=[DataRequired(), Length(1, 128)])
    activist_start = StringField("Activist birth year", validators=[DataRequired(), Length(1, 4), validate_start_year])
    activist_start_BC = BooleanField("Check if activist was born during BC", validators=[Optional()])
    activist_end = StringField("Activist death year", validators=[DataRequired(), Length(1, 5), validate_end_year])
    activist_end_BC = BooleanField("Check if activist died during BC", validators=[Optional()])
    tags = StringField(validators=[DataRequired(), Length(500)])
    content = TextAreaField("Share a few words about how your woman activist has inspired you and others",
                            validators=[DataRequired()])
    activist_url = StringField("Enter a URL to allow others to learn more about your woman activist online",
                               validators=[Optional(), Length(1, 254), validate_url])
    image_url = StringField("Enter an image URL below", validators=[Optional(), validate_image])
    video_url = StringField("Enter a YouTube or Vimeo URL below", validators=[Optional(), validate_video])
    user_first = StringField("User first name", validators=[Optional(), Length(1, 64)])
    user_last = StringField("User last name", validators=[Optional(), Length(1, 64)])
    user_email = StringField("User email", validators=[Optional(), Email(), Length(1, 254)])
    submit = SubmitField('Submit')
